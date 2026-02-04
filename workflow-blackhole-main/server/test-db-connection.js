require('dotenv').config();
const mongoose = require('mongoose');

async function testConnection() {
  try {
    console.log('🔍 Testing MongoDB connection...');
    console.log('📍 URI:', process.env.MONGODB_URI.replace(/:[^:@]+@/, ':****@'));
    
    await mongoose.connect(process.env.MONGODB_URI);
    console.log('✅ Connected to MongoDB successfully!');
    
    // List all collections
    const collections = await mongoose.connection.db.listCollections().toArray();
    console.log('\n📚 Available collections:');
    collections.forEach(col => console.log(`  - ${col.name}`));
    
    // Test write operation
    const TestModel = mongoose.model('Test', new mongoose.Schema({ 
      message: String, 
      timestamp: Date 
    }));
    
    const testDoc = await TestModel.create({
      message: 'Test from workflow-blackhole',
      timestamp: new Date()
    });
    
    console.log('\n✅ Test document created:', testDoc._id);
    
    // Verify read
    const found = await TestModel.findById(testDoc._id);
    console.log('✅ Test document read:', found ? 'SUCCESS' : 'FAILED');
    
    // Cleanup
    await TestModel.deleteOne({ _id: testDoc._id });
    console.log('✅ Test document deleted');
    
    console.log('\n🎉 Database is working correctly!');
    
    await mongoose.connection.close();
    process.exit(0);
  } catch (error) {
    console.error('❌ Database test failed:', error.message);
    process.exit(1);
  }
}

testConnection();
