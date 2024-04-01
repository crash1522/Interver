document.addEventListener('DOMContentLoaded', function () {
    var modal = document.getElementById('login-modal');
    var loginBtn = document.getElementById('go-sign-in'); // 로그인 버튼
    var loginFormButton = document.querySelector('.login-button'); // 로그인 폼 내의 로그인 버튼
    var authLinks = document.querySelector('.auth-links'); // 로그인/회원가입 링크를 담고 있는 div
    var userInfo = document.querySelector('.user-info'); // 사용자 정보 및 로그아웃 링크를 담고 있는 div

    // 로그인 상태 확인 함수
    function isLoggedIn() {
        return localStorage.getItem('isLoggedIn') === 'true';
    }

    // 로그인 상태에 따라 UI 변경 함수
    function toggleUIBasedOnLoginStatus() {
        if (isLoggedIn()) { //로그인 상태로 바꿀려면 !표 붙여야함
            authLinks.style.display = 'none';
            userInfo.style.display = 'flex';
        } else {
            authLinks.style.display = 'flex';
            userInfo.style.display = 'none';
        }
    }

    // 모달 창 열기 함수
    function openModal() {
        modal.style.display = 'block';
        modal.classList.remove('modal-close-animation');
        modal.classList.add('modal-open-animation');
    }

    // 모달 창 닫기 함수
    function closeModal() {
        modal.classList.remove('modal-open-animation');
        modal.classList.add('modal-close-animation');
        setTimeout(() => {
            modal.style.display = 'none';
        }, 500);
    }

    // 모달 외부 클릭 시 모달 창 닫기
    window.onclick = function(event) {
        if (event.target === modal) {
            closeModal();
        }
    };

    loginBtn.onclick = function() {
        openModal();
    };

    if (loginFormButton) {
        loginFormButton.onclick = function(event) {
            localStorage.setItem('isLoggedIn', 'true');
            closeModal();
            toggleUIBasedOnLoginStatus();

            document.getElementById('user-id').value = '';
            document.getElementById('user-password').value = '';
        };
    }

    var logoutButton = document.getElementById('logout');
    if (logoutButton) {
        logoutButton.addEventListener('click', function() {
            localStorage.removeItem('isLoggedIn'); // 로그아웃 상태로 설정
            toggleUIBasedOnLoginStatus(); // UI 업데이트

            // 'home.html' 내용을 AJAX로 가져와 메인 섹션에 삽입
            fetch('/')
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.text();
                })
                .then(html => {
                    document.querySelector('.main').innerHTML = html;
                    // home.html 로딩 후 필요한 추가적인 초기화 로직이 있다면 여기에 구현
                })
                .catch(error => {
                    console.error('Error loading the page: ', error);
                });
        });

    }

    toggleUIBasedOnLoginStatus();

    // 시작하기 버튼 클릭 이벤트
    document.body.addEventListener('click', function(event) {
        // 이벤트가 발생한 요소가 "시작하기" 버튼인지 확인
        if (event.target.classList.contains('start-btn')) {
            if (!isLoggedIn()) {  //로그인 상태로 바꿀려면 !표 빼야함
                openModal(); // 비로그인 상태에서 모달 창 열기
            } else {
                loadServicePage(); // 로그인 상태일 때 service.html 내용 가져오기
            }
        }
    });

    // service.html 내용을 가져와서 페이지에 삽입하는 함수
    function loadServicePage() {
        fetch('api/common/service')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.text();
            })
            .then(html => {
                document.querySelector('.main').innerHTML = html;
                // service.html 로딩 후 필요한 추가적인 초기화 로직이 있다면 여기에 구현
            })
            .catch(error => {
                console.error('Error loading the page: ', error);
            });
    }


    
});

function initializeSignUpForm() {
    const addSkillButton = document.getElementById('addSkillButton');
    const skillInput = document.getElementById('skillInput');
    const skillList = document.getElementById('skillList');
    const skillsHiddenInput = document.getElementById('skillsHiddenInput');

    function updateSkillsInput() {
        const allSkills = Array.from(skillList.querySelectorAll('.skill-item div')).map(skill => skill.textContent);
        skillsHiddenInput.value = allSkills.join(',');
        document.getElementById('skillListPlaceholder').style.display = allSkills.length > 0 ? 'none' : 'block';
    }

    function removeSkill(event) {
        if (event.target.classList.contains('delete-skill')) { // 클래스 이름이 'delete-skill'인 버튼 클릭을 확인
            skillList.removeChild(event.target.closest('.skill-item'));
            updateSkillsInput();
        }
    }

    function addSkill(skill) {
        const skillItem = document.createElement('div');
        skillItem.classList.add('skill-item');
        const skillTextDiv = document.createElement('div');
        skillTextDiv.textContent = skill;

        const deleteButton = document.createElement('button');
        deleteButton.textContent = 'X';
        deleteButton.classList.add('delete-skill'); // 삭제 버튼에 클래스 추가
        skillItem.appendChild(skillTextDiv);
        skillItem.appendChild(deleteButton);

        skillList.appendChild(skillItem);
        updateSkillsInput();
    }

    addSkillButton.addEventListener('click', function() {
        const skill = skillInput.value.trim();
        if (skill) {
            addSkill(skill);
            skillInput.value = '';
        }
    });

    // 이벤트 위임을 사용하여 skillList 내의 모든 삭제 버튼에 대한 클릭 이벤트 처리
    skillList.addEventListener('click', removeSkill);


// 게시물 목록을 생성하는 함수
    function renderPosts(paginatedPosts) {
        const postsList = document.getElementById("postsList");
        postsList.innerHTML = "";
        paginatedPosts.forEach((post) => {
            const row = document.createElement("tr");
            row.innerHTML = `
            <td>${post.title}</td>
            <td>${post.company}</td>
            <td>${post.date}</td>`;
            row.querySelector('td:first-child').addEventListener('click', () => openModal(post));
            postsList.appendChild(row);
        });
    }



// 페이지 로드 시 첫 페이지의 게시물을 렌더링
    document.addEventListener("DOMContentLoaded", () => paginatePosts(currentPage));


// 상세 글 보기를 위한 가상의 예시 데이터
    const postsDetails = {
        // 게시물 ID를 키로 사용
        "1": {
            title: "게시물 제목 1",
            company: "회사명 1",
            date: "2023-01-01",
            content: [
                { question: "질문 1", answer: "답변 1", feedback: "피드백 1" },
                { question: "질문 2", answer: "답변 2", feedback: "피드백 2" },
                // 반복되는 구조...
            ],
            finalFeedback: "전체 피드백 내용"
        },
        // 추가 게시물 상세 정보...
    };

// 모달 열기 함수 수정
    function openModal(post) {
        const modal = document.getElementById("record-modal");
        const modalContent = modal.querySelector(".record-modal-content");
        modalContent.innerHTML = `<p><strong>제목:</strong> ${post.title}</p>
                              <p><strong>회사명:</strong> ${post.company}</p>
                              <p><strong>날짜:</strong> ${post.date}</p>`;

        const postDetail = postsDetails[post.id]; // 가정: post 객체에 id 속성이 있다고 가정
        if (postDetail && postDetail.content) {
            postDetail.content.forEach((item, index) => {
                modalContent.innerHTML += `<div>
                <p><strong>${index + 1}번째 질문:</strong> ${item.question}</p>
                <p><strong>${index + 1}번째 답변:</strong> ${item.answer}</p>
                <p><strong>${index + 1}번째 피드백:</strong> ${item.feedback}</p>
            </div>`;
            });

            // 전체 피드백 추가
            modalContent.innerHTML += `<p><strong>전체 피드백:</strong> ${postDetail.finalFeedback}</p>`;
        }

        modal.style.display = "block";
    }

// 모달 외부 클릭 시 닫기 이벤트 리스너 설정
    window.addEventListener('click', function(event) {
        const modal = document.getElementById("record-modal");
        if (event.target === modal) {
            modal.style.display = "none";
        }
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

    document.getElementById('check-duplicate').addEventListener('click', function() {
        var userId = document.querySelector('[name="userId"]').value; // 사용자가 입력한 아이디 값을 가져옵니다.

        // XMLHttpRequest 객체 생성
        var xhr = new XMLHttpRequest();
        var url = "/api/user/create/is_duplcate"; // 서버의 중복 확인 API 경로
        xhr.open("POST", url, true);
        xhr.setRequestHeader("Content-Type", "application/json");
        
        // 서버로부터 응답을 받았을 때 실행될 함수
        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4) {
                var errorMessageDiv = document.getElementById('duplicate-message');
                var response = JSON.parse(xhr.responseText);
                console.log(response)
                errorMessageDiv.textContent = response.message; // 에러 메시지 표시
                if (response.message == "사용 가능한 아이디입니다.") {
                    errorMessageDiv.style.color = '#4c80f0';   
                }
                else {
                    errorMessageDiv.style.color = 'red';
                }
                errorMessageDiv.style.display = 'block'; // 에러 메시지 보이기
            }
        };
        
        // 서버로 전송할 데이터 구성 및 전송
        var data = JSON.stringify({userid: userId});
        xhr.send(data);
    });

    document.getElementById('signupForm').addEventListener('submit', function(event) {
        event.preventDefault(); // 폼의 기본 제출 동작 방지
    
        // 입력값 수집
        let userid = document.querySelector('[name="userId"]').value;
        let password = document.querySelector('[name="password"]').value;
        let confirm_password = document.querySelector('[name="passwordConfirm"]').value;
        let username = document.querySelector('[name="name"]').value;
        let field = document.querySelector('[name="interest"]').value;
        let skills = JSON.parse(document.getElementById('skillsHiddenInput').value || '[]');
    
        // XMLHttpRequest 객체 생성 및 설정
        var xhr = new XMLHttpRequest();
        var url = "/api/user/create"; // 변경될 수 있음
        xhr.open("POST", url, true);
        xhr.setRequestHeader("Content-Type", "application/json");
    
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4) {
                var errorMessageDiv = document.getElementById('error-message');
                if (xhr.status === 204) {
                    console.log("User created successfully");
                    // 성공 처리 로직: 홈 페이지로 리디렉션
                    window.location.href = '/'; // 홈 페이지 URL로 변경하세요
                } else {
                    console.error("Error creating user: ", xhr.responseText);
                    
                    var message = JSON.parse(xhr.responseText).detail[0].msg.replace("Value error, ", "");
                    errorMessageDiv.textContent = message; // 에러 메시지 표시
                    errorMessageDiv.style.display = 'block'; // 에러 메시지 보이기
                }
            }
        };
    
        // 서버로 전송할 데이터 구성 및 전송
        var data = JSON.stringify({
            userid: userid,
            username: username,
            password: password,
            confirm_password: confirm_password,
            field: field,
            skills: skills
        });
    
        xhr.send(data);
    });
    
    
}


