import {
    BaseEntity,
    Column,
    Entity, ManyToOne,
    PrimaryGeneratedColumn,
} from "typeorm";
import {Movie} from "./Movie";

/**
 * @Entity
 * name: Director
 * implementation: directors
 * replication_overhead: 2
 * columns:
 *   - id
 *   - name
 *   - surname
 */

@Entity('directors')
export class Director extends BaseEntity{
    @PrimaryGeneratedColumn()
    id: number;
    @Column()
    name: string;
    @Column()
    surname: string;

    @ManyToOne(type => Movie, movie => movie.directors_id)
    movies: Movie[];
}
