const mongoose = require('mongoose');
const movieSchema = new mongoose.Schema({
    title: { type: String, required: true },
    description: { type: String, required: true },
    poster: { type: String, required: true }, 
    available: { type: Boolean, default: true }
});

const showSchema = new mongoose.Schema({
    movie: { type: mongoose.Schema.Types.ObjectId, ref: 'Movie', required: true },
    time: { type: Date, required: true },
    uuid: { type: String, unique: true, required: true }
});

const Movie = mongoose.model('Movie', movieSchema);
const Show = mongoose.model('Show', showSchema);

module.exports = { Movie, Show };