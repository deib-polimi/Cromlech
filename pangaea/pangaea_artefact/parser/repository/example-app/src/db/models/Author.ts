import {
    BaseEntity,
    Column,
    Entity, ManyToOne,
    PrimaryGeneratedColumn,
} from "typeorm";
import {Book} from "./Book";

/**
 * @Entity
 * name: Author
 * implementation: authors
 * replication_overhead: 2
 * columns:
 *   - id
 *   - name
 *   - surname
 */

@Entity('authors')
export class Author extends BaseEntity{
    @PrimaryGeneratedColumn()
    id: number;
    @Column()
    name: string;
    @Column()
    surname: string;

    @ManyToOne(type => Book, book => book.authors_id)
    books: Book[];
}
