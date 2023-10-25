import {
    BaseEntity,
    Column,
    Entity, JoinColumn, ManyToOne,
    PrimaryGeneratedColumn,
} from "typeorm";
import {Director} from "./Director";
import {Author} from "./Author";

/**
 * @Entity
 * name: Book
 * implementation: books
 * replication_overhead: 1
 * columns:
 *   - id
 *   - title
 *   - plot_summary
 *   - duration
 *   - directors_id
 * relations:
 *   - entity_name: Author
 *     type: aggregation
 */

@Entity('books')
export class Book extends BaseEntity{
    @PrimaryGeneratedColumn()
    id: number;
    @Column()
    title: string;
    @Column()
    plot_summary: string;
    @Column()
    authors_id: number;

    @ManyToOne(type => Author, author => author.books)
    @JoinColumn({name: "authors_id"})
    author: Author;
}
