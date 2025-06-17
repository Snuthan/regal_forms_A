const express = require('express');
const router = express.Router();

const formFields = [
  { field: 'fullName', question: 'What is your full name?' },
  { field: 'panNumber', question: 'What is your PAN number?' },
  { field: 'bankName', question: 'Which bank are you using for foreign contributions?' }
];

let userResponses = {};
let currentIndex = 0;

router.post('/next', (req, res) => {
  const { answer } = req.body;

  // Save the previous answer
  if (currentIndex > 0) {
    const lastField = formFields[currentIndex - 1].field;
    userResponses[lastField] = answer;
  }

  // End of form
  if (currentIndex >= formFields.length) {
    const finalResponse = { ...userResponses };
    userResponses = {}; // Reset
    currentIndex = 0;
    return res.json({ message: 'Form submitted!', data: finalResponse });
  }

  // Send next question
  const nextQuestion = formFields[currentIndex].question;
  currentIndex++;
  res.json({ question: nextQuestion });
});

module.exports = router;
