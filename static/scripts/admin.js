
function ShowContent(contentId) {
    const contents = document.querySelectorAll('.content');
    contents.forEach(content => {
        content.classList.remove('active'); 
});
    const selectedContent = document.getElementById(contentId);
    selectedContent.classList.add('active');
}



document.getElementById('updateQueryButton').addEventListener('click', function() {
    const currentUrl = new URL(window.location.href);
    //fetch... => category
    currentUrl.searchParams.set('query', 'category'); 

    window.history.pushState({}, '', currentUrl);
});