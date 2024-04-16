document.addEventListener('DOMContentLoaded', function () {
    var modal = document.getElementById('login-modal');


    var loginBtn = document.getElementById('go-sign-in'); // 로그인 버튼
    var loginFormButton = document.querySelector('.login-button'); // 로그인 폼 내의 로그인 버튼
    var authLinks = document.querySelector('.auth-links'); // 로그인/회원가입 링크를 담고 있는 div
    var userInfo = document.querySelector('.user-info'); // 사용자 정보 및 로그아웃 링크를 담고 있는 div
    
    function isTokenExpired(token) {
        const payload = JSON.parse(atob(token.split('.')[1]));
        const now = Date.now() / 1000; // 현재 시간을 초 단위로 변환
        return now > payload.exp;
    }
    
    function isLoggedIn() {
        const token = localStorage.getItem('access_token');
        if (!token) {
            return false;
        }
        return !isTokenExpired(token);
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

// 모달 열기 함수 (범용)
function openModal(modal) {
    if (modal) {
        modal.style.display = 'block';  
        modal.classList.add('modal-open-animation');
        modal.classList.remove('modal-close-animation');
    }
}
function closeModal(modal) {
    if (modal) {
        modal.classList.remove('modal-open-animation');
        modal.classList.add('modal-close-animation');
        setTimeout(() => {
            modal.style.display = 'none';
        }, 500);
    }
}

function openAnswerModal(userAnswerModal) {
    if (userAnswerModal) {
        userAnswerModal.style.display = 'flex';  
        userAnswerModal.classList.add('chat-modal-open-animation2');
        userAnswerModal.classList.remove('chat-modal-close-animation2');
    }
}


function closeAnswerModal(userAnswerModal) {
    if (userAnswerModal) {
        userAnswerModal.classList.remove('chat-modal-open-animation');
        userAnswerModal.classList.add('chat-modal-close-animation');
        setTimeout(() => {
            userAnswerModal.style.display = 'none';
        }, 500);
    }
}
function openQuestionModal(aiQuestionModal) {
            if (aiQuestionModal) {
            aiQuestionModal.style.display = 'flex';  
            aiQuestionModal.classList.remove('chat-modal-close-animation');
            aiQuestionModal.classList.add('chat-modal-open-animation');
            }
        }
function closeQuestionModal(aiQuestionModal) {
    if (aiQuestionModal) {
        aiQuestionModal.classList.remove('chat-modal-open-animation');
        aiQuestionModal.classList.add('chat-modal-close-animation');
        setTimeout(() => {
            aiQuestionModal.style.display = 'none';
        }, 500);
    }
}
    // 모달 외부 클릭 시 모달 창 닫기
    window.onclick = function(event) {
        if (event.target === modal) {
            closeModal(modal);
        }
    };

    loginBtn.onclick = function() {
        openModal(modal);
    };

    if (loginFormButton) {
        loginFormButton.addEventListener('click', function(event) {
            event.preventDefault(); // 폼의 기본 제출 동작을 방지
    
            var userIdElement = document.getElementsByName('user-id')[0];
            var passwordElement = document.getElementsByName('user-password')[0];
            if (userIdElement && passwordElement) {
                var userId = userIdElement.value;
                var password = passwordElement.value;
                // 이후 로직 처리
            } else {
                // 요소가 없는 경우의 처리 로직
                console.error('Form elements not found');
            }

            // 로그인 요청을 위한 URL
            const url = '/api/user/login';
    
            // XMLHttpRequest 객체를 생성합니다.
            var xhr = new XMLHttpRequest();
            xhr.open('POST', url, true); // 비동기 방식으로 요청을 초기화합니다.
    
            // 요청 헤더를 설정합니다.
            xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    
            // 요청의 상태 변경을 처리하기 위한 이벤트 핸들러를 설정합니다.
            xhr.onreadystatechange = function() {
                if (xhr.readyState === 4) { // 요청이 완료되었을 때
                    if (xhr.status === 200) {
                        var data = JSON.parse(xhr.responseText);
                        localStorage.setItem('access_token', data.access_token); // 받은 액세스 토큰 저장
                        localStorage.setItem('userid', data.userid);
                        // localStorage.setItem('user_profile', data.user_profile);
                        // user_profile 객체를 올바르게 문자열로 변환하여 저장
                        localStorage.setItem('user_profile', JSON.stringify(data.user_profile));

                        // 사용자 이름(또는 ID)를 페이지에 표시합니다.
                        document.getElementById('user-name').textContent = data.userid + '님';
                        
                        closeModal(); // 모달 창 닫기
                        toggleUIBasedOnLoginStatus(); // UI 상태 업데이트
                        
                        setTimeout(function() {
                            window.location.href = '/'; // 홈 페이지 URL로 변경
                        }, 500); // 모달 닫힘 애니메이션의 지속 시간에 맞춰 조절하세요.
                    } else {
                        var errorMessageDiv = document.getElementById('login-error-message');
                        var errorResponse = JSON.parse(xhr.responseText);
                        // 에러 메시지 줄바꿈 처리 및 표시
                        errorMessageDiv.innerHTML  = errorResponse.detail.replace(/\n/g, '<br>');
                        errorMessageDiv.style.display = 'block'; // 에러 메시지 보이기
                        console.error('Login failed:', errorResponse.detail);
                    }
                }
            };
            // URLSearchParams 객체를 사용하여 요청 본문을 구성합니다.
            var formData = new URLSearchParams();
            formData.append('username', userId);
            formData.append('password', password);
            console.log('Sending request with body:', formData.toString());
            // 요청을 전송합니다.
            xhr.send(formData.toString());
             // 비밀번호 입력 필드 초기화
             document.getElementById('user-password').value = '';
        });
    }
    
    
    
    var logoutButton = document.getElementById('logout');
    if (logoutButton) {
        logoutButton.addEventListener('click', function() {
            localStorage.removeItem('access_token'); // 액세스 토큰 삭제
            localStorage.removeItem('userid'); // 사용자 ID 삭제
            toggleUIBasedOnLoginStatus(); // UI 업데이트

            // 'home.html' 내용을 AJAX로 가져와 메인 섹션에 삽입
            fetch('/api/user/logout')
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.text();
                })
                .then(html => {
                    window.location.href = '/';
                    // document.querySelector('.main').innerHTML = html;
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
                openModal(modal); // 비로그인 상태에서 모달 창 열기
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
                // 애니메이션 클래스 추가
                document.querySelector('.main').classList.add('animate-fade-in');

                // 애니메이션 종료 후 클래스 제거 (옵션)
                document.querySelector('.main').addEventListener('animationend', function() {
                    this.classList.remove('animate-fade-in');
                });
                // service.html 로딩 후 필요한 추가적인 초기화 로직이 있다면 여기에 구현
            })
            .catch(error => {
                console.error('Error loading the page: ', error);
            });
    }
    
    // move.js 와 script.js 연결
    document.addEventListener('pageLoaded', function(event) {
        if (event.detail.page === 'interview_chat') {
            const questionData = event.detail.data; // Here you access the passed questionData
            console.log('Received question data:', questionData);
            ChatPage(questionData); // Pass the questionData to ChatPage
        }
    });
    



    // AI 질문 모달에서 MP3 재생 시작 및 이벤트 핸들링
    async function playAIQuestion(questionData) {
        document.getElementById("loadingModal").style.display = "block";
        var aiQuestionModal = document.getElementById('ai-question-modal'); // AI 질문 모달 요소 선택
        const response = await fetch('/api/handler/text_to_speech', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ content: questionData.content }) //content: text
        });
        document.getElementById("loadingModal").style.display = "none";
        // AI 질문 모달 열기
        openQuestionModal(aiQuestionModal);
    
        if (response.ok) {
            const blob = await response.blob(); // 음성 데이터를 blob으로 받기
            const url = URL.createObjectURL(blob); // Blob 객체로부터 URL 생성
            const audio = new Audio(url);
            audio.play(); // 오디오 재생
            audio.onended = function() {
                // AI 질문 모달 닫기
                closeQuestionModal(aiQuestionModal);
                // 사용자 답변 모달 열기
                handleUserAnswer(questionData);
            };
        } else {
            console.error('Failed to convert text to speech');
        }
    }
    

    function handleUserAnswer(questionData) {
        var userAnswerModal = document.getElementById('user-answer-modal'); // 사용자 답변 모달 요소 선택
        document.getElementById('ai-question-textbox').textContent = questionData.content;
        openAnswerModal(userAnswerModal);
        
        // 사용자의 오디오 입력 장치에 접근 권한을 요청
        navigator.mediaDevices.getUserMedia({ audio: true })
            .then(stream => {
                let mediaRecorder = new MediaRecorder(stream);
                let audioChunks = [];
        
                mediaRecorder.ondataavailable = event => {
                    audioChunks.push(event.data);
                };
        
                mediaRecorder.onstop = () => {
                    const audioBlob = new Blob(audioChunks, { type: 'audio/mp3' });
                    mediaRecorder.stream.getTracks().forEach(track => track.stop()); // 마이크 사용 중지
        
                    const formData = new FormData();
                    formData.append('file', audioBlob, 'recorded_audio.mp3');
                    const accessToken = localStorage.getItem('access_token');
        
                    fetch(`/api/answer/user_answer_create/${questionData.id}`, {
                        method: 'POST',
                        body: formData,
                        headers: {
                            'Authorization': `Bearer ${accessToken}` // 인증 토큰 헤더에 추가
                        },
                    }).then(response => {
                        if (!response.ok) {
                            throw new Error('Network response was not ok');
                        }
                        return response.json();
                    }).then(data => {
                        console.log(data);
                        const userAnswerTextbox = document.querySelector('.user-answer-textbox');
                        if (userAnswerTextbox) {
                            userAnswerTextbox.textContent = data.content;
                        }
                    
                        // answer_id를 사용하여 새 질문을 요청
                        fetch(`/api/question/question_create/${data.record_id}`, { 
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                                'Authorization': `Bearer ${localStorage.getItem('access_token')}`  
                            },
                            body: JSON.stringify({ before_answer_id: data.id })  // data.id는 answer_id
                        })
                        .then(response => response.json())
                        .then(questionData => {
                            console.log('New question received:', questionData);
                            closeAnswerModal(userAnswerModal);
                            playAIQuestion(questionData);
                        })
        
                    audioChunks = [];
                })};
        
                // 녹음 시작
                mediaRecorder.start();
        
                // 마이크 아이콘에 클릭 이벤트 리스너 추가
                const micIcon = document.getElementById('user_recording_circlein');
                micIcon.addEventListener('click', () => {
                    mediaRecorder.stop(); // 사용자가 마이크 아이콘을 클릭하면 녹음 중지
                });
            })
            .catch(error => {
                console.error("Microphone access was denied: ", error);
            });
    }
    

    
    
    function ChatPage(questionData) {
        fetch('api/common/interview_chat')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.text();
            })
            .then(html => {
                document.querySelector('.main').innerHTML = html;
                // 사용자의 오디오 입력 장치에 접근 권한을 요청
                navigator.mediaDevices.getUserMedia({ audio: true })
                .then(() => { 
                    playAIQuestion(questionData);
                })
                .catch(error => {
                    console.error("Microphone access was denied: ", error);
                });
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
        let skillsInputValue = document.getElementById('skillsHiddenInput').value;
        // 값을 배열로 변환합니다.
        let skills = skillsInputValue ? skillsInputValue.split(',') : [];
        
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


