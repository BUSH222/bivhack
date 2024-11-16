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
