const STADIUM = { lat: 35.19408, lng: 129.06152 };

const CATEGORY_CODES = {
  관광: 'AT4',
  식당: 'FD6',
  숙소: 'AD5',
  카페: 'CE7',
};

const CATEGORY_NAMES = {
  AT4: '관광',
  FD6: '식당',
  AD5: '숙소',
  CE7: '카페',
};

let kakaoPromise;

export { STADIUM };

export function loadKakao() {
  if (window.kakao?.maps?.services) return Promise.resolve(window.kakao);
  if (kakaoPromise) return kakaoPromise;

  kakaoPromise = new Promise((resolve, reject) => {
    const key = import.meta.env.VITE_KAKAO_JS_KEY;
    if (!key) {
      kakaoPromise = undefined;
      reject(new Error('frontend/.env에 VITE_KAKAO_JS_KEY를 넣어 주세요.'));
      return;
    }

    const script = document.createElement('script');
    script.src = `https://dapi.kakao.com/v2/maps/sdk.js?appkey=${key}&libraries=services&autoload=false`;
    script.async = true;
    script.onload = () => window.kakao.maps.load(() => resolve(window.kakao));
    script.onerror = () => {
      kakaoPromise = undefined;
      reject(new Error('카카오맵 스크립트를 불러오지 못했습니다.'));
    };
    document.head.appendChild(script);
  });

  return kakaoPromise;
}

function toPlace(doc) {
  return {
    id: doc.id,
    name: doc.place_name,
    address: doc.road_address_name || doc.address_name,
    category: CATEGORY_NAMES[doc.category_group_code] || '기타',
    tags: [doc.category_group_name].filter(Boolean),
    distance: doc.distance ? `경기장까지 ${doc.distance}m` : '',
    lat: Number(doc.y),
    lng: Number(doc.x),
    visit_minutes: 60,
    opening_time: '10:00:00',
    closing_time: '22:00:00',
  };
}

export function searchKakaoPlaces(query, category) {
  return loadKakao().then((kakao) => new Promise((resolve, reject) => {
    const places = new kakao.maps.services.Places();
    const options = {
      location: new kakao.maps.LatLng(STADIUM.lat, STADIUM.lng),
      radius: 10000,
      sort: kakao.maps.services.SortBy.DISTANCE,
    };
    const code = CATEGORY_CODES[category];
    const keyword = query.trim();

    const done = (data, status) => {
      if (status === kakao.maps.services.Status.ZERO_RESULT) {
        resolve([]);
        return;
      }
      if (status !== kakao.maps.services.Status.OK) {
        reject(new Error('장소 검색에 실패했습니다.'));
        return;
      }
      resolve(data.map(toPlace));
    };

    if (!keyword) {
      places.categorySearch(code || 'AT4', done, options);
      return;
    }

    if (code) options.category_group_code = code;
    places.keywordSearch(keyword, done, options);
  }));
}
