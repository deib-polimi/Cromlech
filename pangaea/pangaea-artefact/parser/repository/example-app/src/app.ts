import express from 'express';
import * as bodyParser from 'body-parser';
import {Movie} from "./db/models/Movie";
import {connect} from "./db/db";
import {Director} from "./db/models/Director";
import {Book} from "./db/models/Book";

connect();

const app = express();
app.use(bodyParser.json({
    limit: '50mb',
    verify(req: any, res, buf, encoding) {
        req.rawBody = buf;
    }
}));

app.get('/', (req, res) => res.send('Hello World!'));


/**
 * @Operation
 * name: createMovie
 * integrity: high
 * frequency: 4
 * forced_entities:
 *   - Movie
 * entities:
 *   - entity_name: Movie
 *     access_mode: write
 *   - entity_name: Director
 *     access_mode: read
 */
// CREATE
app.post('/movies', async (req,res) => {
    const movie = new Movie();
    movie.title = req.body.title;
    movie.plot_summary = req.body.plot_summary;
    movie.duration = req.body.duration;
    movie.directors_id = req.body.directors_id;
    await movie.save();
    res.send(movie);
});

/**
 * @Operation
 * name: retrieveMovie
 * integrity: low
 * frequency: 7
 * entities:
 *   - entity_name: Movie
 *     access_mode: read
 *   - entity_name: Director
 *     access_mode: read
 */
// READ
app.get('/movies', async (req,res) => {
    const movies = await Movie.find();
    res.send(movies);
});

/**
 * @Operation
 * name: updateMovie
 * integrity: low
 * frequency: 3
 * forced_entities:
 *   - Movie
 * entities:
 *   - entity_name: Movie
 *     access_mode: read-write
 *   - entity_name: Director
 *     access_mode: write
 */
// UPDATE
app.put('/movies/:id', async (req,res) => {
    const movie = await Movie.findOne({
        where: {
            id: req.params.id
        }
    });
    if (movie){
        if (req.body.title) {
            movie.title = req.body.title;
        }
        if (req.body.plot_summary){
            movie.plot_summary = req.body.plot_summary;
        }
        if (req.body.duration){
            movie.duration = req.body.duration;
        }
        if (req.body.directors_id){
            movie.directors_id = req.body.directors_id;
        }
        await movie.save();
        res.send(movie);
    } else {
        res.status(404).send({message: "Movie not found"})
    }
});

/**
 * @Operation
 * name: createDirector
 * integrity: high
 * frequency: 2
 * forced_entities:
 *   - Director
 * entities:
 *   - entity_name: Director
 *     access_mode: write
 */
// CREATE
app.post('/directors', async (req,res) => {
    const director = new Director();
    director.name = req.body.name;
    director.surname = req.body.surname;
    await director.save();
    res.send(director);
});

/**
 * @Operation
 * name: createBook
 * integrity: high
 * frequency: 3
 * forced_entities:
 *   - Book
 * entities:
 *   - entity_name: Book
 *     access_mode: write
 *   - entity_name: Author
 *     access_mode: read
 */
// CREATE
app.post('/books', async (req,res) => {
    const book = new Book();
    book.title = req.body.title;
    book.plot_summary = req.body.plot_summary;
    book.authors_id = req.body.authors_id;
    await book.save();
    res.send(book);
});

/**
 * @Operation
 * name: retrieveBooks
 * integrity: low
 * frequency: 8
 * entities:
 *   - entity_name: Book
 *     access_mode: read
 *   - entity_name: Author
 *     access_mode: read
 */
// READ
app.get('/books', async (req,res) => {
    const books = await Book.find();
    res.send(books);
});

/**
 * @Operation
 * name: retrieveAll
 * integrity: low
 * frequency: 10
 * entities:
 *   - entity_name: Book
 *     access_mode: read
 *   - entity_name: Author
 *     access_mode: read
 *   - entity_name: Movie
 *     access_mode: read
 *   - entity_name: Director
 *     access_mode: read
 */
// READ
app.get('/all', async (req,res) => {
    const books = await Book.find();
    const movies = await Movie.find();
    res.send(books, movies);
});

export {app};
