let currentStep = 0;
const totalSteps = 4;
const steps = document.querySelectorAll('.step');
const progressBar = document.querySelector('.progress-bar');
const nextBtn = document.querySelector('.next-btn');
const prevBtn = document.querySelector('.prev-btn');


function updateProgress() {
  steps.forEach((step, index) => {
    if (index < currentStep) {
      step.classList.add('completed');
      step.classList.remove('active');
    } else if (index === currentStep) {
      step.classList.add('active');
      step.classList.remove('completed');
    } else {
      step.classList.remove('active', 'completed');
    }
  });


  progressBar.style.width = `${(currentStep / totalSteps) * 100}%`;


  prevBtn.disabled = currentStep === 0;
  nextBtn.disabled = currentStep === totalSteps;
}


nextBtn.addEventListener('click', () => {
  if (currentStep < totalSteps) {
    currentStep++;
    updateProgress();
  }
});

prevBtn.addEventListener('click', () => {
  if (currentStep > 0) {
    currentStep--;
    updateProgress();
  }
});


updateProgress();


////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////FUNCTIONS TO CREATE FIELDS///////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

const mainContainer = document.getElementById('main-container');
const addHeaderButton = document.getElementById('add-header-btn');


function createHeader() {

  const headerSection = document.createElement('div');
  headerSection.className = 'header-section';


  const header = document.createElement('h2');
  header.className = 'header';
  header.textContent = `Новый заголовок`;

  const LiList = document.createElement("ul");
 
  LiList.className = "ListOfFields";

  const addFieldButton = document.createElement('button');
  addFieldButton.textContent = '+ Добавить поле';
  addFieldButton.onclick = () => addTextField(LiList);

  LiList.appendChild(addFieldButton);
  headerSection.appendChild(addFieldButton)
  headerSection.appendChild(LiList);


  mainContainer.appendChild(headerSection);
}

function addTextField(section) {
  const textField = document.createElement('input');
  textField.type = 'text';
  textField.placeholder = 'Введите текст';
  section.appendChild(textField);
}


addHeaderButton.onclick = createHeader;
