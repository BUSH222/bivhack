function ShowContent(contentId) {
    const contents = document.querySelectorAll('.content');
    contents.forEach(content => {
        content.classList.remove('active'); 
});
    const selectedContent = document.getElementById(contentId);
    selectedContent.classList.add('active');
}