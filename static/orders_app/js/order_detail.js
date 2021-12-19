const grouppedCount = JSON.parse(document.getElementById('groupped-count').textContent);

const colors = { 
  'nok': 'red',
  'pro': 'orange',
  'ass': 'skyblue',
  'pkd': 'green'
}

console.log(grouppedCount);


function translateList(qs){
  let data = {};
  if (qs.length > 0){
      qs.forEach(x => {
          data[x.status] = x.status__count;
        })
      
        let sum = Object.values(data).reduce((t, n) => t + n);
        Object.keys(data).forEach(x => {
            data[x] = data[x]/sum * 100;
        })
    }
    
    return data;
}



function createProgressBar(data){

        mainBar = document.querySelector('.main-bar');
        Object.keys(data).forEach(x => {
          smallBar = document.createElement('div');
          smallBar.classList.add('bar-element');
          smallBar.style.width = data[x] + '%';
          smallBar.style.backgroundColor = colors[x];
          smallBar.innerText = x;
          mainBar.appendChild(smallBar);
        })
}

document.addEventListener('DOMContentLoaded', (event) => {
  createProgressBar(translateList(grouppedCount));
})