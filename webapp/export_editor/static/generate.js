(function(){

document.getElementById('generate-button').addEventListener('click', () => {
  console.log('Generating');
  
  const settings = [...document.querySelectorAll('input[data-submit]')].map(input => {
    const setting = input.dataset.submit;
    const value = input.value;

    return {setting, value};
  });

  console.log(settings);
});

})()
