const axios = require('axios');

const BACKEND_URL = 'http://localhost:8001';
const API = `${BACKEND_URL}/api`;

async function testNavigation() {
  try {
    console.log('Testing persona creation...');
    
    const response = await axios.post(`${API}/personas`, {
      starting_method: 'demographics',
      name: `Test Navigation ${new Date().toLocaleDateString()}`
    });
    
    console.log('✅ Persona created successfully:', response.data.id);
    console.log('✅ Navigate to: /persona-wizard?id=' + response.data.id + '&method=demographics');
    
    return true;
  } catch (error) {
    console.error('❌ Error creating persona:', error.message);
    if (error.response) {
      console.error('Response data:', error.response.data);
    }
    return false;
  }
}

testNavigation();