import {
    BaseEntity,
    Column,
    Entity, JoinColumn, ManyToOne,
    PrimaryGeneratedColumn,
} from "typeorm";
import {Director} from "./Director";

/**
 * @Entity
 * name: Movie
 * implementation: movies
 * replication_overhead: 1
 * columns:
 *   - id
 *   - title
 *   - plot_summary
 *   - duration
 *   - directors_id
 * relations:
 *   - entity_name: Director
 *     type: aggregation
 */

@Entity('movies')
export class Movie extends BaseEntity{
    @PrimaryGeneratedColumn()
    id: number;
    @Column()
    title: string;
    @Column()
    plot_summary: string;
    @Column()
    duration: number;
    @Column()
    directors_id: number;

    @ManyToOne(type => Director, director => director.movies)
    @JoinColumn({name: "directors_id"})
    director: Director;
}
