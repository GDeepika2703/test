const {MongoClient} = require('mongodb')
const mongoconfig = require('../config/mongodb')

const client = new MongoClient(mongoconfig.url);

async function connectDB() {
    try {
        await client.connect();
        console.log("Connected to MongoDB!");
        return client;
    } catch (e) {
        console.error(e);
    }
}

module.exports ={
    client,
    connectDB
}