exports.handler = async (event, context) => {
  try {
    const { body } = event;
    const formData = JSON.parse(body);

    // Process formData as needed
    console.log('Form Data:', formData);

    return {
      statusCode: 200,
      body: JSON.stringify({ message: 'Form submitted successfully' }),
    };
  } catch (error) {
    console.error('Error processing form:', error);
    return {
      statusCode: 500,
      body: JSON.stringify({ error: 'Internal Server Error' }),
    };
  }
};
