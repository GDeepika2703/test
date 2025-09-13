const { sendPushNotification } = require('./routes/insert'); // adjust path if needed

const testToken = "cYc1HcOPReCDcZOdOzY6bF:APA91bGKqb_jc3Pqpze7gD4a-fCr9K6G8VmuSZLbq7w89fW6hrPBNYae_EdhmaQCko7DQOC0de_6dIMK024mO1ljKz9RuiFC00TBI3ZXqOaJfMATk5kL-DI";

sendPushNotification(testToken, "Test Notification ✅", "This is a test message from your server.");
