const posts = [
    { id: "1", title: "게시물 제목 1", company: "회사명 1", date: "2023-01-01" },
    { id: "2", title: "게시물 제목 2", company: "회사명 2", date: "2023-01-02" },
    { id: "3", title: "게시물 제목 3", company: "회사명 3", date: "2023-01-03" },
    { id: "4", title: "게시물 제목 4", company: "회사명 4", date: "2023-01-03" },
    { id: "5", title: "게시물 제목 5", company: "회사명 5", date: "2023-01-03" },
    { id: "6", title: "게시물 제목 6", company: "회사명 6", date: "2023-01-03" },
    { id: "7", title: "게시물 제목 7", company: "회사명 7", date: "2023-01-03" },
    { id: "8", title: "게시물 제목 8", company: "회사명 8", date: "2023-01-03" },
    // 추가 게시물 데이터...
];

const postsPerPage = 5;
let currentPage = 1;

function paginatePosts(page) {
    const startIndex = (page - 1) * postsPerPage;
    const endIndex = startIndex + postsPerPage;
    const paginatedPosts = posts.slice(startIndex, endIndex);

    renderPosts(paginatedPosts);
    renderPaginationButtons();
}

function renderPosts(paginatedPosts) {
    const postsList = document.getElementById("postsList");
    postsList.innerHTML = "";
    paginatedPosts.forEach((post) => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${post.title}</td>
            <td>${post.company}</td>
            <td>${post.date}</td>`;
        // row.querySelector('td:first-child').addEventListener('click', () => openModal(post));
        postsList.appendChild(row);
    });
}

function renderPaginationButtons() {
    const totalPages = Math.ceil(posts.length / postsPerPage);
    const pagination = document.getElementById("pagination");
    pagination.innerHTML = "";

    for (let i = 1; i <= totalPages; i++) {
        const button = document.createElement("a");
        button.innerText = i;
        button.href = "#";
        button.addEventListener("click", (e) => {
            e.preventDefault();
            currentPage = i;
            paginatePosts(currentPage);
        });

        if (i === currentPage) {
            button.classList.add("active");
        }

        pagination.appendChild(button);
    }
}