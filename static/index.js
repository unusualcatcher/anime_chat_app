function toggleOptions() {
    const optionsSidebar = document.querySelector('.options-sidebar');
    optionsSidebar.classList.toggle('show-sidebar');
  }
  
  window.addEventListener('resize', function() {
    const optionsSidebar = document.querySelector('.options-sidebar');
    if (window.innerWidth > 768) {
      optionsSidebar.classList.remove('show-sidebar');
    }
  });
  