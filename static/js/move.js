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
                // 애니메이션 클래스 추가
                document.querySelector('.main').classList.add('animate-slide-in-up');

                // 애니메이션 종료 후 클래스 제거 (애니메이션을 다시 재생할 수 있도록)
                document.querySelector('.main').addEventListener('animationend', function() {
                    document.querySelector('.main').classList.remove('animate-slide-in-up');
                });
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

    document.getElementById('go-my-page').addEventListener('click', function(event) {
        event.preventDefault(); // 기본 이벤트 방지
    
        // 'api/common/mypage'로부터 마이페이지 내용을 AJAX로 가져옴
        fetch('api/common/mypage')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.text();
        })
        .then(html => {
            // 마이페이지 HTML 내용을 .main에 삽입
            document.querySelector('.main').innerHTML = html;
            
            // localStorage에서 user_profile 정보를 가져옴
            const userProfileString = localStorage.getItem('user_profile');
            // 문자열을 객체로 변환
            const userProfile = JSON.parse(userProfileString);
            if (userProfile) {
                // 여기서 페이지가 이미 로드되었으므로, 직접 DOM 요소에 접근하여 값을 업데이트할 수 있음
                // 'input[name="userId"]' 등의 선택자는 실제 요소의 name 속성과 일치해야 함
                document.querySelector('input[name="userId"]').value = userProfile.userid || '';
                document.querySelector('input[name="name"]').value = userProfile.username || '';
                document.querySelector('input[name="interest"]').value = userProfile.field || '';
    
                const skillsContainer = document.getElementById('skillList');
                // 기술 목록을 콤마와 공백으로 구분된 문자열로 조합합니다.
                const skillsText = userProfile.skills.join(', ');
                skillsContainer.textContent = skillsText; // 또는 innerHTML, 이 경우 HTML 태그도 사용 가능합니다.

            
                
            } else {
                console.error('User profile data is not available in localStorage.');
            }
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
            loadPage('interview_prepare'); // 모의 면접 준비 페이지 로드
        } else if (event.target.id === 'find-log-btn') {
            event.preventDefault(); // 기본 이벤트 방지
            loadPage('interview_all_repo'); // 면접 기록 페이지 로드
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
            if (page === 'interview_prepare') {
                updateToggleStatus();
            } else if (page === 'interview_all_repo') {
                paginatePosts(currentPage);
            }
            // 페이지 로딩 후 필요한 추가적인 스크립트 초기화나 처리가 필요하면 여기에 추가
        })
        .catch(error => {
            console.error('Error loading the page: ', error);
        });
    }

    function fetchUserProfile() {
        // 여기서는 예시로 XMLHttpRequest를 사용합니다.
        // 실제로는 인증 방식에 맞춰 Authorization 헤더 등을 추가해야 합니다.
        var xhr = new XMLHttpRequest();
        var url = "/api/user/profile"; // 사용자 정보 API 엔드포인트
        let token = localStorage.getItem('accessToken');
        xhr.open("GET", url, true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.setRequestHeader("Authorization", "Bearer " + token); // "Bearer " 접두사 추가
    
        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4 && xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                populateUserProfile(response); // HTML에 사용자 정보를 채우는 함수 호출
            }
        };
        xhr.send();
    
    }
    
    function populateUserProfile(data) {
        // HTML 요소에 데이터 채우기
        document.querySelector('[name="userId"]').value = data.userid;
        document.querySelector('[name="name"]').value = data.username;
        document.querySelector('[name="interest"]').value = data.field;
        
        // 스킬 리스트 처리
        var skillsContainer = document.getElementById('skillList');
        data.skills.forEach(skill => {
            var skillDiv = document.createElement('div');
            skillDiv.textContent = skill;
            skillsContainer.appendChild(skillDiv);
        });
    }
    
    
    
    
    