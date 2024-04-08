// 가상의 데이터
const records = [
    { create_date: '2024-01-10', company_name: 'ABC Corporation' },
    { create_date: '2024-01-15' },
    { create_date: '2024-01-20', company_name: 'XYZ Inc.' },
    { create_date: '2024-01-25', company_name: 'Tech Innovations' },
    { create_date: '2024-02-01' }, // 회사명이 없는 경우
    { create_date: '2024-02-10', company_name: 'New Horizons Ltd' },
    { create_date: '2024-02-15', company_name: 'Future Tech' },
    { create_date: '2024-02-20' },
    { create_date: '2024-02-25', company_name: 'Creative Solutions' },
    { create_date: '2024-03-01' }, // 회사명이 없는 경우
    { create_date: '2024-03-05', company_name: 'Alpha Enterprises' },
    { create_date: '2024-03-10' },
    { create_date: '2024-03-15', company_name: 'Innovative Designs' },
    { create_date: '2024-03-20', company_name: 'Market Leaders Inc.' },
    { create_date: '2024-03-25' } // 회사명이 없는 경우
];

const recordsPerPage = 5;
let currentPage = 1;

function displayRecords(page) {
    const startIndex = (page - 1) * recordsPerPage;
    const endIndex = startIndex + recordsPerPage;
    const recordsToShow = records.slice(startIndex, endIndex);

    const listElement = document.querySelector('.records-list');
    listElement.innerHTML = ''; // 기록 목록을 초기화
    recordsToShow.forEach(record => {
        const date = new Date(record.create_date);
        const formattedDate = `${date.getFullYear()}년 ${date.getMonth() + 1}월 ${date.getDate()}일`;
    
        const companyName = record.company_name || ''; // 회사명이 없으면 '회사명 없음'을 표시
        const recordElement = document.createElement('div');
        recordElement.classList.add('record');
        
        // innerHTML 대신 textContent를 사용해 회사명이 정확히 텍스트로 처리되도록 함
        recordElement.textContent = `${formattedDate} ${companyName} 모의면접`;
        
        listElement.appendChild(recordElement);
    });
    
    
}


function setupPagination(totalRecords, recordsPerPage) {
    const pageCount = Math.ceil(totalRecords / recordsPerPage);
    const paginationContainer = document.querySelector('.pagination');
    paginationContainer.innerHTML = ''; // 페이지네이션 버튼 초기화

    for (let i = 1; i <= pageCount; i++) {
        const button = document.createElement('button');
        button.textContent = i;

        // 현재 페이지 버튼에 'active' 클래스 추가
        if (currentPage === i) {
            button.classList.add('active');
        }

        button.addEventListener('click', function() {
            // 모든 버튼에서 'active' 클래스 제거
            document.querySelectorAll('.pagination button').forEach(btn => {
                btn.classList.remove('active');
            });
            // 클릭된 버튼에 'active' 클래스 추가
            this.classList.add('active');

            currentPage = i;
            displayRecords(currentPage);
        });
        
        paginationContainer.appendChild(button);
    }
}


