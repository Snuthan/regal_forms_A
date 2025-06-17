const express = require('express');
const router = express.Router();

const forms = {
  "FC": {
    "title": "Form FC - Foreign Contribution",
    "checklist": ["PAN card", "Bank details", "Signature"],
    "sample_link": "https://yourdomain.com/forms/form-fc-sample.pdf"
  },
  "XYZ": {
    "title": "Form XYZ - Export Declaration",
    "checklist": ["Invoice", "Shipping Bill"],
    "sample_link": "https://yourdomain.com/forms/form-xyz-sample.pdf"
  }
};

router.get('/:formName', (req, res) => {
  const formName = req.params.formName.toUpperCase();
  const form = forms[formName];

  if (!form) {
    return res.status(404).send("Form not found");
  }

  res.json(form);
});

module.exports = router;
