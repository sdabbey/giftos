const buttons = document.querySelector('.verification-modal section.content ul.buttons');
const numberField = document.querySelector(".verification-modal section.content input[type='number']");
const fields = document.querySelectorAll('.verification-modal section.content ul.buttons li button');

setInterval(getNum, 100);
buttons.addEventListener('click', test);


for (n=0; n < 4; n++){
    fields[n].addEventListener('click', test);
}

function getNum(){
    const nums = numberField.value;
    for(n=0; n < 4; n++){
        if(nums[n] >= 0){
            fields[n].innerHTML = nums[n];
        }
        else{
            fields[n].innerHTML = ''
        }
    }
}


function test(e){
    e.preventDefault();
    numberField.focus();
}





