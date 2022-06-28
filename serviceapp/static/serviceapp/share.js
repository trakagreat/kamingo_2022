const shareData = {
    title: 'Founde a service',
    text: 'Check out this very Good service you can use',
    url: "{% url 'service-detail-page' service.slug %}"
  }
  
  const btn = document.querySelector('.share');
  const resultPara = document.querySelector('.result');
  
  // Share must be triggered by "user activation"
  btn.addEventListener('click', async () => {
    try {
      await navigator.share(shareData)
      resultPara.textContent = 'shared successfully'
    } catch(err) {
      resultPara.textContent = ''
    }
  });
  