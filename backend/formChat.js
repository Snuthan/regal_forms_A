const readline = require('readline');

const formFields = [
  { field: 'fullName', question: 'What is your full name?' },
  { field: 'panNumber', question: 'What is your PAN number?' },
  { field: 'bankName', question: 'Which bank are you using for foreign contributions?' }
];

const userResponses = {};
let currentIndex = 0;

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

const askNextQuestion = () => {
  if (currentIndex < formFields.length) {
    rl.question(formFields[currentIndex].question + ' ', (answer) => {
      userResponses[formFields[currentIndex].field] = answer;
      currentIndex++;
      askNextQuestion();
    });
  } else {
    console.log('\n✅ Form filled successfully! Collected data:');
    console.log(userResponses);
    rl.close();
  }
};

console.log('📝 Starting chat-based form...');
askNextQuestion();
