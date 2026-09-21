from datetime import datetime, time, timedelta
from typing import Any, Optional


class ScheduleService:
    """경기 전후 관광지를 greedy insertion으로 배치한다."""

    CONGESTION_WEIGHT = 5.0
    PARTICIPANT_WEIGHT = 0.1
    HIGH_CONGESTION_THRESHOLD = 70.0

    def build_schedule(self, request: dict[str, Any]) -> dict[str, Any]:
        participant_count = request["participant_count"]
        game = request["game"]
        start_point = request["start_point"]
        end_point = request["end_point"]
        places = request["places"]
        travel_times = request["travel_times"]
        congestion_cache = request.get("congestion_cache", {})

        game_start = self._datetime(game["start_time"])
        start_time = self._datetime(start_point["arrival_time"])
        accommodation = end_point.get("accommodation")
        return_transport = end_point.get("return_transport")
        if accommodation is not None:
            if end_point.get("accommodation_deadline") is None:
                raise ValueError("숙소 도착 제한시간이 필요합니다.")
            end_location = accommodation
            end_time = self._datetime(end_point["accommodation_deadline"])
            final_anchor = (
                self._anchor("return_transport", return_transport["location"], self._datetime(return_transport["departure_time"]))
                if return_transport is not None else None
            )
        elif return_transport is not None:
            end_location = return_transport["location"]
            end_time = self._datetime(return_transport["departure_time"])
            final_anchor = None
        else:
            raise ValueError("숙소 또는 귀가 교통편 중 하나는 필요합니다.")

        if start_time >= game_start:
            raise ValueError("출발지 도착시간은 경기 시작시간보다 빨라야 합니다.")
        if game_start >= end_time:
            raise ValueError("귀가 교통편 또는 숙소 도착 제한시간은 경기 시작시간보다 늦어야 합니다.")

        start_anchor = self._anchor("start", start_point["location"], start_time)
        game_anchor = self._anchor("game", game["stadium"], game_start)
        end_anchor = self._anchor("accommodation" if accommodation is not None else "end", end_location, end_time)

        before, after, rejected = self._classify_places(
            places, start_anchor, game_anchor, end_anchor, travel_times
        )
        before_timeline, before_failed = self._insert_greedy(
            before, start_anchor, game_anchor, travel_times, congestion_cache, participant_count
        )
        after_timeline, after_failed = self._insert_greedy(
            after, game_anchor, end_anchor, travel_times, congestion_cache, participant_count
        )

        if final_anchor is not None:
            after_timeline = self._set_schedule_times(after_timeline + [final_anchor], travel_times)
            if after_timeline[-1]["arrival_time"] > final_anchor["time"]:
                raise ValueError("숙소에서 귀가 교통편까지 이동할 시간이 부족합니다.")

        return {
            "participant_count": participant_count,
            "anchors": {
                "start": start_anchor,
                "game": game_anchor,
                "end": end_anchor,
                **({"return_transport": final_anchor} if final_anchor is not None else {}),
            },
            "items": before_timeline[:-1] + after_timeline,
            "unplaced_places": rejected + before_failed + after_failed,
        }

    def _classify_places(self, places, start_anchor, game_anchor, end_anchor, travel_times):
        before, after, rejected = [], [], []
        for place in places:
            before_feasible = self._can_fit_direct(place, start_anchor, game_anchor, travel_times)
            after_feasible = self._can_fit_direct(place, game_anchor, end_anchor, travel_times)
            if before_feasible:
                before.append(place)
            elif after_feasible:
                after.append(place)
            else:
                rejected.append(self._failed(place, "경기 전후 어느 구간에도 배치할 수 없습니다."))
        return before, after, rejected

    def _insert_greedy(self, places, start_anchor, end_anchor, travel_times, congestion_cache, participant_count):
        scheduled = [start_anchor]
        remaining = list(places)
        failed = []

        while remaining:
            best = None
            for place in remaining:
                for position in range(1, len(scheduled) + 1):
                    candidate = self._try_insertion(
                        scheduled, position, place, end_anchor, travel_times,
                        congestion_cache, participant_count
                    )
                    if candidate is None:
                        continue
                    cost, candidate_schedule = candidate
                    if best is None or cost < best[2]:
                        best = (place, position, cost, candidate_schedule)

            if best is None:
                failed.extend(self._failed(place, "영업시간 또는 다음 고정 지점 때문에 배치할 수 없습니다.") for place in remaining)
                break

            place, _, _, scheduled = best
            remaining.remove(place)

        scheduled.append(end_anchor)
        return self._set_schedule_times(scheduled, travel_times), failed

    def _try_insertion(self, scheduled, position, place, end_anchor, travel_times, congestion_cache, participant_count):
        candidate = scheduled[:]
        candidate.insert(position, self._place_node(place))
        candidate.append(end_anchor)
        timed = self._set_schedule_times(candidate, travel_times)

        for node in timed[1:-1]:
            if node["type"] == "place" and not self._within_opening_hours(node):
                return None
        if timed[-1]["arrival_time"] > end_anchor["time"]:
            return None

        place_node = timed[position]
        hour = str(self._datetime(place_node["arrival_time"]).hour)
        congestion = self._congestion_rate(congestion_cache.get(place["id"]), hour)
        place_node["congestion"] = congestion
        place_node["congestion_warning"] = congestion >= self.HIGH_CONGESTION_THRESHOLD
        cost = self._travel_minutes(candidate, position, travel_times)
        cost += congestion * self.CONGESTION_WEIGHT * (1 + participant_count * self.PARTICIPANT_WEIGHT)
        return cost, timed[:-1]

    def _set_schedule_times(self, nodes, travel_times):
        timed = []
        for index, node in enumerate(nodes):
            node_copy = dict(node)
            if index == 0:
                current = node_copy["time"]
                node_copy["arrival_time"] = current
                node_copy["departure_time"] = current
            else:
                previous = timed[-1]
                travel = self._travel_between(previous, node_copy, travel_times)
                arrival = previous["departure_time"] + timedelta(minutes=travel)
                if node_copy["type"] == "place":
                    arrival = self._adjust_for_opening(node_copy, arrival)
                node_copy["arrival_time"] = arrival
                node_copy["departure_time"] = (
                    arrival + timedelta(minutes=node_copy["visit_minutes"])
                    if node_copy["type"] == "place" else arrival
                )
            timed.append(node_copy)
        return timed

    def _can_fit_direct(self, place, start, end, travel_times):
        place_node = self._place_node(place)
        arrival = start["time"] + timedelta(minutes=self._travel_between(start, place_node, travel_times))
        arrival = self._adjust_for_opening(place_node, arrival)
        departure = arrival + timedelta(minutes=place["visit_minutes"])
        can_reach_end = departure + timedelta(minutes=self._travel_between(place_node, end, travel_times)) <= end["time"]
        return can_reach_end and self._within_opening_hours({**place_node, "arrival_time": arrival, "departure_time": departure})

    def _within_opening_hours(self, node):
        opening = self._parse_time(node.get("opening_time"))
        closing = self._parse_time(node.get("closing_time"))
        if opening is None or closing is None:
            return True
        return opening <= node["arrival_time"].time() and node["departure_time"].time() <= closing

    def _adjust_for_opening(self, node, arrival):
        opening = self._parse_time(node.get("opening_time"))
        if opening is not None and arrival.time() < opening:
            return datetime.combine(arrival.date(), opening)
        return arrival

    def _travel_between(self, previous, current, travel_times):
        return self._travel_value(previous["location"]["id"], current["location"]["id"], travel_times)

    def _travel_minutes(self, nodes, position, travel_times):
        previous, current, next_node = nodes[position - 1:position + 2]
        return (
            self._travel_between(previous, current, travel_times)
            + self._travel_between(current, next_node, travel_times)
            - self._travel_between(previous, next_node, travel_times)
        )

    @staticmethod
    def _travel_value(source, target, travel_times):
        try:
            value = travel_times[source][target]
        except KeyError as error:
            raise ValueError(f"이동시간이 누락되었습니다: {source} -> {target}") from error
        if value < 0:
            raise ValueError("이동시간은 0 이상이어야 합니다.")
        return value

    @staticmethod
    def _congestion_rate(value, hour: str) -> float:
        """Accept daily API results, legacy hourly maps, and missing data."""
        if value is None:
            return 0.0
        if isinstance(value, (int, float)):
            return float(value)
        if not isinstance(value, dict):
            return 0.0
        if value.get("rate") is not None:
            return float(value["rate"])
        hourly_value = value.get(hour, 0.0)
        return float(hourly_value) if isinstance(hourly_value, (int, float)) else 0.0

    @staticmethod
    def _place_node(place):
        return {
            "type": "place", "id": place["id"], "name": place["name"],
            "location": place["location"], "visit_minutes": place["visit_minutes"],
            "opening_time": place.get("opening_time"), "closing_time": place.get("closing_time"),
        }

    @staticmethod
    def _anchor(node_type, location, node_time):
        return {"type": node_type, "location": location, "time": node_time,
                "arrival_time": node_time, "departure_time": node_time}

    @staticmethod
    def _failed(place, reason):
        return {"id": place["id"], "name": place["name"], "reason": reason}

    @staticmethod
    def _datetime(value):
        return value if isinstance(value, datetime) else datetime.fromisoformat(value)

    @staticmethod
    def _parse_time(value) -> Optional[time]:
        return value if value is None or isinstance(value, time) else time.fromisoformat(value)