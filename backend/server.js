const express = require('express');
const app = express();
const authRoutes = require('./routes/auth');
const formDiscoveryRoutes = require('./routes/formDiscovery'); 
const chatRoutes = require('./routes/chat');
app.use('/api/chat', chatRoutes);
// 👈 new line

app.use(express.json());
app.use('/api/auth', authRoutes);
app.use('/api/forms', formDiscoveryRoutes); // 👈 new line

app.listen(3000, () => console.log("Server running on http://localhost:3000"));
