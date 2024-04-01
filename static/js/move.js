document.addEventListener('DOMContentLoaded', function () {
// home으로 이동 --------------------------
    document.querySelector('.logo-name').addEventListener('click', function (e) {
        e.preventDefault(); // 기본 이벤트 차단

        // AJAX 요청 설정
        var xhr = new XMLHttpRequest();
        xhr.open('GET', '/', true); // 여기서 'home.html'은 서버상의 경로에 맞게 조정해야 합니다.
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 200) {
                // 응답으로 받은 HTML에서 main 내용 추출
                var parser = new DOMParser();
                var doc = parser.parseFromString(xhr.responseText, "text/html");
                var newMainContent = doc.querySelector('.main').innerHTML;

                // 현재 문서의 main 섹션 내용 교체
                document.querySelector('.main').innerHTML = newMainContent;

                // 필요한 경우 여기서 추가적인 스크립트 초기화를 수행
            }
        };
        xhr.send();
    });
// home으로 이동 끝 --------------------------

// 회원가입 폼으로 이동 끝 시작 -----------------------
    document.getElementById('go-sign-up').addEventListener('click', function (e) {
        e.preventDefault(); // 기본 이벤트(링크 이동) 차단

        // AJAX 요청 생성 및 설정
        var xhr = new XMLHttpRequest();
        xhr.open('GET', 'api/common/sign_up', true);
        xhr.onreadystatechange = function () {
            // 요청이 성공적으로 완료되었는지 확인
            if (xhr.readyState === 4 && xhr.status === 200) {
                // main 섹션의 내용을 응답으로 받은 HTML로 교체
                document.querySelector('.main').innerHTML = xhr.responseText;
                initializeSignUpForm();
            }
        };
        xhr.send(); // 요청 전송
    });
// 회원가입 폼으로 이동 끝 --------------------------

// 로그인 모달에서 회원가입 이동 ----------------------
    document.getElementById('move-sign-up').addEventListener('click', function (e) {
        e.preventDefault(); // 기본 이벤트 차단

        // AJAX 요청 설정
        var xhr = new XMLHttpRequest();
        xhr.open('GET', 'api/common/sign_up', true); // 'sign-up.html'의 실제 경로로 변경해야 함
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 200) {
                // 응답으로 받은 HTML에서 main 내용 추출
                var parser = new DOMParser();
                var doc = parser.parseFromString(xhr.responseText, "text/html");
                var newMainContent = doc.querySelector('.main').innerHTML;

                // 현재 문서의 main 섹션 내용 교체
                document.querySelector('.main').innerHTML = newMainContent;
                // 로그인 모달 창 숨김
                document.getElementById('login-modal').style.display = 'none';
                // 필요한 경우 여기서 추가적인 스크립트 초기화를 수행
                initializeSignUpForm();
            }
        };
        xhr.send();
    });
// 로그인 모달에서 회원가입 이동 끝 ----------------------

// 회원가입 폼 제출 후 홈으로 시작 ----------------------
//     document.getElementById('signupForm').addEventListener('submit', function (e) {
//         e.preventDefault(); // 폼의 기본 제출 동작 차단
//
//         // FormData 객체를 사용해 폼 데이터를 쉽게 수집
//         var formData = new FormData(this);
//
//         // DB로 데이터를 제출하는 부분 (현재는 주석 처리)
//         /*
//         fetch('/submit-form-url', {
//             method: 'POST',
//             body: formData
//         })
//         .then(response => response.json())
//         .then(data => {
//             console.log('Success:', data);
//             // 데이터 제출 성공 시 home.html로 내용을 교체
//             return fetch('home.html');
//         })
//         .then(response => response.text())
//         .then(html => {
//             document.querySelector('.main').innerHTML = html;
//             // 추가적인 초기화 작업이 필요하면 여기서 실행
//         })
//         .catch((error) => {
//             console.error('Error:', error);
//         });
//         */
//
//         // DB 제출 부분을 건너뛰고 바로 home.html 로드 (예시)
//         fetch('../html/home.html')
//             .then(response => response.text())
//             .then(html => {
//                 document.querySelector('.main').innerHTML = html;
//
//                 // home.html 로드 후 필요한 초기화 작업을 여기서 실행
//             })
//             .catch((error) => {
//                 console.error('Error:', error);
//             });
//     });
// 회원가입 폼 제출 후 홈으로 끝 ----------------------

// 서비스페이지로 이동 시작 --------------------------
    // 'go-service' 링크 클릭 이벤트 처리
    document.getElementById('go-service').addEventListener('click', function(event) {
        event.preventDefault(); // 기본 이벤트 방지

        // 'service.html' 내용을 AJAX로 가져와 메인 섹션에 삽입
        fetch('api/common/service') // 경로 확인 필요
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.text();
            })
            .then(html => {
                document.querySelector('.main').innerHTML = html;
                // 추가적인 스크립트 초기화나 처리가 필요하면 여기에 추가
            })
            .catch(error => {
                console.error('Error loading the page: ', error);
            });
    });

    // 서비스페이지로 이동 끝 --------------------------

// 마이페이지로 이동 시작 --------------------------
    document.getElementById('go-my-page').addEventListener('click', function(event) {
        event.preventDefault(); // 기본 이벤트 방지

        // 'service.html' 내용을 AJAX로 가져와 메인 섹션에 삽입
        fetch('api/common/mypage') // 경로 확인 필요
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.text();
            })
            .then(html => {
                document.querySelector('.main').innerHTML = html;
                // 추가적인 스크립트 초기화나 처리가 필요하면 여기에 추가
            })
            .catch(error => {
                console.error('Error loading the page: ', error);
            });
    });
    // 마이페이지로 이동 끝 --------------------------

    // 모의면접 사전입력, 모의면접 기록 페이지 이동 시작 --------------------------
    document.querySelector('.main').addEventListener('click', function(event) {
        // 'move-interview-btn' 버튼이 클릭된 경우에만 핸들러 실행
        if (event.target.id === 'move-interview-btn') {
            event.preventDefault(); // 기본 이벤트 방지
            loadPage('interview_prepare.html'); // 모의 면접 준비 페이지 로드
        } else if (event.target.id === 'find-log-btn') {
            event.preventDefault(); // 기본 이벤트 방지
            loadPage('interview_all_repo.html'); // 면접 기록 페이지 로드
        }
    });
    // 모의면접 사전입력, 모의 면접 기록 페이지 이동 시작 --------------------------

});

// 페이지 내용을 AJAX로 가져와 메인 섹션에 삽입하는 함수
function loadPage(page) {
    fetch(`api/common/${page}`) // 경로 확인 필요
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.text();
        })
        .then(html => {
            document.querySelector('.main').innerHTML = html;
            initPage();
            if (page === 'interview/interview_prepare.html') {
                updateToggleStatus();
            } else if (page === 'interview/interview_all_repo.html') {
                paginatePosts(currentPage);
            }
            // 페이지 로딩 후 필요한 추가적인 스크립트 초기화나 처리가 필요하면 여기에 추가
        })
        .catch(error => {
            console.error('Error loading the page: ', error);
        });
}

