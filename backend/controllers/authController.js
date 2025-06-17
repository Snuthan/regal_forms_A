const jwt = require('jsonwebtoken');
const bcrypt = require('bcryptjs');

const users = []; // temporary in-memory array

exports.signup = (req, res) => {
  const { email, password } = req.body;
  const hashed = bcrypt.hashSync(password, 10);
  users.push({ email, password: hashed });
  res.send("User registered!");
};

exports.login = (req, res) => {
  const { email, password } = req.body;
  const user = users.find(u => u.email === email);
  if (!user || !bcrypt.compareSync(password, user.password))
    return res.status(401).send("Invalid credentials");

  const token = jwt.sign({ email }, "secretkey", { expiresIn: "1h" });
  res.json({ token });
};
