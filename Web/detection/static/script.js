// script.js
document.getElementById('upload-form').onsubmit = function() {
  document.getElementById('loading-message').style.display = 'flex'; // 로딩 메시지 표시
};
document.getElementById('upload-form').addEventListener('submit', function() {
    document.getElementById('loading-message').style.display = 'block';
});
// 스크롤 이벤트에 반응하는 애니메이션 추가
window.addEventListener('scroll', () => {
    const elements = document.querySelectorAll('.card, .btn');
    elements.forEach(element => {
        if (element.getBoundingClientRect().top < window.innerHeight) {
            element.style.opacity = 1;
            element.style.transform = 'translateY(0)';
        }
    });
});
