/**
 * @Entity
 * name: Apple
 * implementation: apples
 * replication_overhead: 1
 * columns:
 *   - id
 *   - iss
 *   - sub
 *   - aud
 *   - iat
 *   - exp
 *   - created_at
 *   - updated_at
 * relations:
 *   - entity_name: User
 *     type: composition
 */

/**
 * @Entity
 * name: Application
 * implementation: application
 * replication_overhead: 1
 * columns:
 *   - id
 *   - job_offers_id
 *   - users_id
 *   - score
 *   - employers_id
 *   - view
 *   - status
 *   - created_at
 *   - updated_at
 *   - university_name
 *   - university_tag
 *   - universities_id
 *   - course_name
 *   - courses_id
 *   - city_name
 *   - city_tag
 *   - cities_id
 *   - country_name
 *   - country_tag
 *   - countries_id
 *   - story_url
 *   - applied_at
 * relations:
 *   - entity_name: JobOffer
 *     type: aggregation
 *   - entity_name: User
 *     type: aggregation
 */

/**
 * @Entity
 * name: CareerDay
 * implementation: career_days
 * replication_overhead: 1
 * columns:
 *   - id
 *   - start_date
 *   - end_date
 *   - logo_medias_id
 *   - welcome_message
 *   - when_message
 *   - not_in_target_message
 *   - universities_id
 *   - created_at
 *   - updated_at
 * relations:
 *   - entity_name: Content
 *     type: composition
 *   - entity_name: Media
 *     type: aggregation
 *   - entity_name: Institute
 *     type: aggregation
 */

/**
 * @Entity
 * name: CareerDayRegistration
 * implementation: career_days_registrations
 * replication_overhead: 1
 * columns:
 *   - id
 *   - career_days_id
 *   - users_id
 *   - created_at
 *   - updated_at
 * relations:
 *   - entity_name: CareerDay
 *     type: aggregation
 *   - entity_name: User
 *     type: aggregation
 */

/**
 * @Entity
 * name: CheckIn
 * implementation: check_ins
 * replication_overhead: 1
 * columns:
 *   - id
 *   - events_id
 *   - users_id
 *   - employers_id
 *   - view
 *   - users_status
 *   - university_name
 *   - university_tag
 *   - universities_id
 *   - city_name
 *   - city_tag
 *   - cities_id
 *   - country_name
 *   - country_tag
 *   - countries_id
 *   - course_name
 *   - courses_id
 *   - created_at
 *   - updated_at
 *   - cv
 *   - comments
 * relations:
 *   - entity_name: Event
 *     type: aggregation
 *   - entity_name: User
 *     type: aggregation
 */

/**
 * @Entity
 * name: City
 * implementation: cities
 * replication_overhead: 1
 * columns:
 *   - id
 *   - name
 *   - tag
 *   - countries_id
 *   - lat
 *   - lng
 *   - population
 *   - view
 *   - created_at
 *   - updated_at
 * relations:
 *   - entity_name: Country
 *     type: aggregation
 */

/**
 * @Entity
 * name: CommunityArticle
 * implementation: community_articles
 * replication_overhead: 1
 * columns:
 *   - id
 *   - contents_id
 *   - streams_id
 *   - seo_title
 *   - status
 *   - created_at
 *   - updated_at
 * relations:
 *   - entity_name: Content
 *     type: composition
 *   - entity_name: Stream
 *     type: aggregation
 */

/**
 * @Entity
 * name: Content
 * implementation: contents
 * replication_overhead: 1
 * columns:
 *   - id
 *   - title
 *   - text
 *   - tags
 *   - type
 *   - slug
 *   - media_sets_id
 *   - filter_definitions_id
 *   - sort_date
 *   - created_at
 *   - updated_at
 * relations:
 *   - entity_name: MediaSet
 *     type: aggregation
 *   - entity_name: FilterDefinition
 *     type: aggregation
 */

/**
 * @Entity
 * name: Country
 * implementation: countries
 * replication_overhead: 1
 * columns:
 *   - id
 *   - name
 *   - tag
 *   - manage_graduation_vote
 *   - code
 *   - view
 *   - created_at
 *   - updated_at
 */

/**
 * @Entity
 * name: CountryHasQualification
 * implementation: country_has_qualifications
 * replication_overhead: 1
 * columns:
 *   - id
 *   - countries_id
 *   - qualifications_id
 *   - created_at
 *   - updated_at
 *   - qualifications_id
 * relations:
 *   - entity_name: Country
 *     type: composition
 *   - entity_name: Qualification
 *     type: composition
 */

/**
 * @Entity
 * name: Course
 * implementation: courses
 * replication_overhead: 1
 * columns:
 *   - id
 *   - name
 *   - view
 *   - tag
 *   - tag_2
 *   - tag_3
 *   - study_tag
 *   - macro_study_tag
 *   - qualifications_id
 *   - universities_id
 *   - created_at
 *   - updated_at
 *   - shared
 * relations:
 *   - entity_name: Qualification
 *     type: aggregation
 *   - entity_name: Institute
 *     type: aggregation
 */

/**
 * @Entity
 * name: Education
 * implementation: educations
 * replication_overhead: 1
 * columns:
 *   - id
 *   - university_name
 *   - university_tag
 *   - universities_id
 *   - course_name
 *   - course_tag
 *   - courses_id
 *   - faculty_tag
 *   - qualification_name
 *   - qualifications_id
 *   - cities_id
 *   - city_name
 *   - city_tag
 *   - countries_id
 *   - country_name
 *   - country_tag
 *   - users_id
 *   - created_at
 *   - updated_at
 *   - study_tags_id
 *   - is_current
 *   - status
 *   - votes_id
 *   - vote
 *   - avg
 *   - finished_at
 *   - expected_finished_at
 *   - started_at
 * relations:
 *   - entity_name: User
 *     type: aggregation
 *   - entity_name: StudyTag
 *     type: aggregation
 *   - entity_name: Qualification
 *     type: aggregation
 *   - entity_name: Institute
 *     type: aggregation
 *   - entity_name: Vote
 *     type: aggregation
 */

/**
 * @Entity
 * name: EmployerHasOperator
 * implementation: employer_has_operators
 * replication_overhead: 1
 * columns:
 *   - id
 *   - employers_id
 *   - users_id
 *   - created_at
 *   - updated_at
 * relations:
 *   - entity_name: User
 *     type: composition
 */

/**
 * @Entity
 * name: Event
 * implementation: events
 * replication_overhead: 1
 * columns:
 *   - id
 *   - title
 *   - description
 *   - welcome_message
 *   - slug
 *   - img
 *   - logo
 *   - employers_id
 *   - operators_id
 *   - status
 *   - created_at
 *   - updated_at
 * relations:
 *   - entity_name: User
 *     type: aggregation
 *   - entity_name: Stream
 *     type: aggregation
 */

/**
 * @Entity
 * name: Experience
 * implementation: experiences
 * replication_overhead: 1
 * columns:
 *   - id
 *   - title
 *   - description
 *   - experience_types_id
 *   - users_id
 *   - view
 *   - started_at
 *   - finished_at
 *   - created_at
 *   - updated_at
 * relations:
 *   - entity_name: ExperienceType
 *     type: aggregation
 *   - entity_name: User
 *     type: aggregation
 */

/**
 * @Entity
 * name: ExperienceType
 * implementation: experience_types
 * replication_overhead: 1
 * columns:
 *   - id
 *   - name_en
 *   - name_it
 *   - name_es
 *   - name_fr
 *   - view
 *   - created_at
 *   - updated_at
 */

/**
 * @Entity
 * name: Facebook
 * implementation: facebooks
 * replication_overhead: 1
 * columns:
 *   - id
 *   - facebook_id
 *   - access_token
 *   - expiration_date
 *   - scopes
 *   - created_at
 *   - updated_at
 * relations:
 *   - entity_name: User
 *     type: composition
 */

/**
 * @Entity
 * name: Filter
 * implementation: filters
 * replication_overhead: 1
 * columns:
 *   - id
 *   - filter_definitions_id
 *   - course_tags
 *   - faculty_tags
 *   - universities_ids
 *   - countries_ids
 *   - cities_ids
 *   - locations_ids
 *   - industries_ids
 *   - tags
 *   - use_profile_institutes_id
 *   - use_profile_countries_id
 *   - use_profile_cities_id
 *   - use_profile_locations_id
 *   - use_profile_study_tag
 *   - created_at
 *   - updated_at
 * relations:
 *   - entity_name: FilterDefinition
 *     type: composition
 */

/**
 * @Entity
 * name: FilterDefinition
 * implementation: filter_definitions
 * replication_overhead: 1
 * columns:
 *   - id
 *   - name
 *   - created_at
 *   - updated_at
 */

/**
 * @Entity
 * name: Google
 * implementation: googles
 * replication_overhead: 1
 * columns:
 *   - id
 *   - alg
 *   - at_hash
 *   - aud
 *   - azp
 *   - google
 *   - iss
 *   - kid
 *   - sub
 *   - typ
 *   - created_at
 *   - updated_at
 * relations:
 *   - entity_name: User
 *     type: composition
 */

/**
 * @Entity
 * name: Industry
 * implementation: industries
 * replication_overhead: 1
 * columns:
 *   - id
 *   - name_it
 *   - name_en
 *   - name_es
 *   - name_fr
 *   - view
 *   - created_at
 *   - updated_at
 */

/**
 * @Entity
 * name: Institute
 * implementation: institutes
 * replication_overhead: 1
 * columns:
 *   - id
 *   - name
 *   - view
 *   - tag
 *   - img
 *   - cities_id
 *   - estimated_target
 *   - created_at
 *   - updated_at
 * relations:
 *   - entity_name: City
 *     type: aggregation
 */

/**
 * @Entity
 * name: Interview
 * implementation: interviews
 * replication_overhead: 1
 * columns:
 *   - id
 *   - applications_id
 *   - operators_id
 *   - status
 *   - booking_id
 *   - url
 *   - samba_private_url
 *   - date
 * relations:
 *   - entity_name: Application
 *     type: aggregation
 *   - entity_name: User
 *     type: aggregation
 */

/**
 * @Entity
 * name: JobOffer
 * implementation: job_offers
 * replication_overhead: 1
 * columns:
 *   - id
 *   - position
 *   - sectors_id
 *   - types_id
 *   - cities_id
 *   - industries_id
 *   - users_id
 *   - description
 *   - requirements
 *   - img
 *   - view
 *   - has_story
 *   - job_video
 *   - job_img
 *   - job_detail_img
 *   - job_video_thumbnail
 *   - locations_id
 *   - external_url
 *   - career_days_id
 *   - created_at
 *   - updated_at
 *   - status
 * relations:
 *   - entity_name: User
 *     type: aggregation
 *   - entity_name: City
 *     type: aggregation
 *   - entity_name: Type
 *     type: aggregation
 *   - entity_name: Industry
 *     type: aggregation
 *   - entity_name: Sector
 *     type: aggregation
 */

/**
 * @Entity
 * name: Language
 * implementation: languages
 * replication_overhead: 1
 * columns:
 *   - id
 *   - name_it
 *   - name_en
 *   - name_fr
 *   - name_es
 *   - view
 *   - created_at
 *   - updated_at
 */

/**
 * @Entity
 * name: LanguageLevel
 * implementation: language_levels
 * replication_overhead: 1
 * columns:
 *   - id
 *   - name_it
 *   - name_en
 *   - name_fr
 *   - name_es
 *   - view
 *   - value
 *   - created_at
 *   - updated_at
 */

/**
 * @Entity
 * name: MacroStudyTag
 * implementation: macro_study_tags
 * replication_overhead: 1
 * columns:
 *   - id
 *   - name_it
 *   - name_en
 *   - name_es
 *   - name_fr
 *   - tag
 *   - created_at
 *   - updated_at
 */

/**
 * @Entity
 * name: Media
 * implementation: medias
 * replication_overhead: 1
 * columns:
 *   - id
 *   - alt
 *   - caption
 *   - height
 *   - width
 *   - size
 *   - url
 *   - mimetype
 *   - created_at
 *   - updated_at
 * relations:
 *   - entity_name: MediaSet
 *     type: aggregation
 */

/**
 * @Entity
 * name: MediaSet
 * implementation: media_sets
 * replication_overhead: 1
 * columns:
 *   - id
 *   - name
 *   - created_at
 *   - updated_at
 */

/**
 * @Entity
 * name: Post
 * implementation: posts
 * replication_overhead: 1
 * columns:
 *   - id
 *   - slug
 *   - article_title
 *   - article_abstract
 *   - article_img
 *   - article_video
 *   - article_video_thumbnail
 *   - published_at
 *   - type
 *   - status
 *   - users_id
 *   - campaigns_id
 *   - view
 *   - sponsored
 *   - created_at
 *   - updated_at
 *   - streams_id
 *   - contents_id
 * relations:
 *   - entity_name: Content
 *     type: composition
 *   - entity_name: User
 *     type: aggregation
 *   - entity_name: Stream
 *     type: aggregation
 */

/**
 * @Entity
 * name: Profile
 * implementation: profiles
 * replication_overhead: 1
 * columns:
 *   - id
 *   - country
 *   - home_page
 *   - claim
 *   - description
 *   - lifestyle
 *   - cover_img
 *   - cover_video
 *   - employer_data
 *   - work_with_us_data
 *   - work_with_us_data_override
 *   - posts_threshold
 *   - users_id
 *   - industries_id
 *   - created_at
 *   - updated_at
 * relations:
 *   - entity_name: User
 *     type: composition
 *   - entity_name: Industry
 *     type: aggregation
 */

/**
 * @Entity
 * name: ProfileMoment
 * implementation: moments
 * replication_overhead: 1
 * columns:
 *   - id
 *   - url
 *   - profiles_id
 *   - created_at
 *   - updated_at
 * relations:
 *   - entity_name: Profile
 *     type: aggregation
 */

/**
 * @Entity
 * name: Qualification
 * implementation: qualifications
 * replication_overhead: 1
 * columns:
 *   - id
 *   - name
 *   - graduation_vote_min
 *   - graduation_vote_max
 *   - exams_vote_min
 *   - exams_vote_max
 *   - is_post_graduate
 *   - created_at
 *   - updated_at
 */

/**
 * @Entity
 * name: Sector
 * implementation: sectors
 * replication_overhead: 1
 * columns:
 *   - id
 *   - name_en
 *   - name_it
 *   - name_es
 *   - name_fr
 *   - view
 *   - created_at
 *   - updated_at
 */

/**
 * @Entity
 * name: Skill
 * implementation: skills
 * replication_overhead: 1
 * columns:
 *   - id
 *   - name_it
 *   - name_en
 *   - name_fr
 *   - name_es
 *   - view
 *   - created_at
 *   - updated_at
 */

/**
 * @Entity
 * name: SkillLevel
 * implementation: skill_levels
 * replication_overhead: 1
 * columns:
 *   - id
 *   - name_it
 *   - name_en
 *   - name_fr
 *   - name_es
 *   - view
 *   - value
 *   - created_at
 *   - updated_at
 */

/**
 * @Entity
 * name: Stream
 * implementation: streams
 * replication_overhead: 1
 * columns:
 *   - id
 *   - slug
 *   - description
 *   - locale
 *   - title
 *   - stream_type
 *   - stream_private
 *   - stream_career_day
 *   - priority
 *   - order
 *   - institutes_id
 *   - faculty_tag
 *   - course_tag
 *   - stream_course
 *   - cities_id
 *   - sectors_id
 *   - countries_id
 *   - tags
 *   - filter_definitions_id
 * relations:
 *   - entity_name: Institute
 *     type: aggregation
 *   - entity_name: Industry
 *     type: aggregation
 *   - entity_name: Sector
 *     type: aggregation
 *   - entity_name: Country
 *     type: aggregation
 *   - entity_name: City
 *     type: aggregation
 *   - entity_name: FilterDefinition
 *     type: aggregation
 */

/**
 * @Entity
 * name: StudyTag
 * implementation: study_tags
 * replication_overhead: 1
 * columns:
 *   - id
 *   - tag
 *   - name_en
 *   - name_it
 *   - name_es
 *   - name_fr
 *   - created_at
 *   - updated_at
 *   - macro_study_tags_id
 * relations:
 *   - entity_name: MacroStudyTag
 *     type: aggregation
 */

/**
 * @Entity
 * name: Type
 * implementation: types
 * replication_overhead: 1
 * columns:
 *   - id
 *   - name_it
 *   - name_en
 *   - name_es
 *   - name_fr
 *   - view
 *   - created_at
 *   - updated_at
 */

/**
 * @Entity
 * name: User
 * implementation: users
 * replication_overhead: 1
 * columns:
 *   - id
 *   - role
 *   - name
 *   - surname
 *   - email
 *   - password
 *   - contact_phone
 *   - contact_email
 *   - contact_address
 *   - revoked_tokens
 *   - img
 *   - location
 *   - birthdate
 *   - language
 *   - view
 *   - slug
 *   - status
 *   - nationality
 *   - courses_id
 *   - created_at
 *   - updated_at
 * relations:
 *   - entity_name: Industry
 *     type: aggregation
 */

/**
 * @Entity
 * name: UserHasLanguage
 * implementation: user_has_languages
 * replication_overhead: 1
 * columns:
 *   - id
 *   - languages_id
 *   - users_id
 *   - language_levels_id
 *   - created_at
 *   - updated_at
 * relations:
 *   - entity_name: User
 *     type: composition
 *   - entity_name: Language
 *     type: composition
 *   - entity_name: LanguageLevel
 *     type: composition
 */

/**
 * @Entity
 * name: UserHasSkill
 * implementation: user_has_skills
 * replication_overhead: 1
 * columns:
 *   - id
 *   - skills_id
 *   - users_id
 *   - skill_levels_id
 *   - created_at
 *   - updated_at
 * relations:
 *   - entity_name: User
 *     type: composition
 *   - entity_name: Skill
 *     type: composition
 *   - entity_name: SkillLevel
 *     type: composition
 */

/**
 * @Entity
 * name: Vote
 * implementation: votes
 * replication_overhead: 1
 * columns:
 *   - id
 *   - name
 *   - value
 *   - qualifications_id
 *   - created_at
 *   - updated_at
 * relations:
 *   - entity_name: Qualification
 *     type: aggregation
 */

/**
 * @Entity
 * name: Webinar
 * implementation: webinars
 * replication_overhead: 1
 * columns:
 *   - id
 *   - contents_id
 *   - duration
 *   - employers_id
 *   - sectors_id
 *   - samba_sessions_id
 *   - video_medias_id
 *   - image_medias_id
 *   - recording_media_sets_id
 *   - created_at
 *   - updated_at
 * relations:
 *   - entity_name: Content
 *     type: composition
 *   - entity_name: Sector
 *     type: aggregation
 *   - entity_name: MediaSet
 *     type: aggregation
 *   - entity_name: User
 *     type: aggregation
 */

/**
 * @Entity
 * name: WebinarParticipation
 * implementation: webinar_participation
 * replication_overhead: 1
 * columns:
 *   - id
 *   - webinars_id
 *   - users_id
 *   - employers_id
 *   - viewed
 *   - state
 *   - downloaded
 *   - samba_private_url
 *   - university_name
 *   - university_tag
 *   - universities_id
 *   - city_name
 *   - city_tag
 *   - cities_id
 *   - country_name
 *   - country_tag
 *   - countries_id
 *   - courses_id
 *   - study_tags_id
 *   - created_at
 *   - updated_at
 * relations:
 *   - entity_name: Webinar
 *     type: composition
 *   - entity_name: User
 *     type: composition
 */

/**
 * @Operation
 * name: AppleV1
 * integrity: high
 * frequency: 5
 * forced_entities:
 *   - Apple
 * entities:
 *   - entity_name: Apple
 *     access_mode: write
 *   - entity_name: User
 *     access_mode: write
 *   - entity_name: Education
 *     access_mode: write
 *   - entity_name: Institute
 *     access_mode: read
 *   - entity_name: StudyTag
 *     access_mode: read
 */

/**
 * @Operation
 * name: ChangePassword
 * integrity: low
 * frequency: 3
 * forced_entities:
 *   - User
 * entities:
 *   - entity_name: User
 *     access_mode: write
 */

/**
 * @Operation
 * name: Facebook
 * integrity: high
 * frequency: 6
 * forced_entities:
 *   - Facebook
 * entities:
 *   - entity_name: User
 *     access_mode: write
 *   - entity_name: Facebook
 *     access_mode: write
 *   - entity_name: Education
 *     access_mode: write
 *   - entity_name: Institute
 *     access_mode: read
 *   - entity_name: StudyTag
 *     access_mode: read
 */

/**
 * @Operation
 * name: ForgotPassword
 * integrity: low
 * frequency: 3
 * forced_entities:
 *   - User
 * entities:
 *   - entity_name: User
 *     access_mode: read
 */

/**
 * @Operation
 * name: Google
 * integrity: high
 * frequency: 6
 * forced_entities:
 *   - Google
 * entities:
 *   - entity_name: User
 *     access_mode: write
 *   - entity_name: Google
 *     access_mode: write
 *   - entity_name: Education
 *     access_mode: write
 *   - entity_name: Institute
 *     access_mode: read
 *   - entity_name: StudyTag
 *     access_mode: read
 */

/**
 * @Operation
 * name: Login
 * integrity: high
 * frequency: 6
 * forced_entities:
 *   - User
 * entities:
 *   - entity_name: User
 *     access_mode: read
 */

/**
 * @Operation
 * name: Logout
 * integrity: high
 * frequency: 4
 * forced_entities:
 *   - User
 * entities:
 *   - entity_name: User
 *     access_mode: write
 */

/**
 * @Operation
 * name: ResetPassword
 * integrity: low
 * frequency: 3
 * forced_entities:
 *   - User
 * entities:
 *   - entity_name: User
 *     access_mode: write
 */

/**
 * @Operation
 * name: RetrieveCommunityArticles
 * integrity: low
 * frequency: 4
 * forced_entities:
 *   - CommunityArticle
 * entities:
 *   - entity_name: CommunityArticle
 *     access_mode: read
 *   - entity_name: Content
 *     access_mode: read
 *   - entity_name: Stream
 *     access_mode: read
 */

/**
 * @Operation
 * name: RetrieveContentsIdFromSlug
 * integrity: low
 * frequency: 5
 * forced_entities:
 *   - Content
 * entities:
 *   - entity_name: Content
 *     access_mode: read
 *   - entity_name: User
 *     access_mode: read
 */

/**
 * @Operation
 * name: Signup
 * integrity: high
 * frequency: 4
 * forced_entities:
 *   - User
 * entities:
 *   - entity_name: User
 *     access_mode: write
 *   - entity_name: Education
 *     access_mode: write
 *   - entity_name: Institute
 *     access_mode: read
 *   - entity_name: StudyTag
 *     access_mode: read
 */

/**
 * @Operation
 * name: applyJobOffer
 * integrity: low
 * frequency: 9
 * forced_entities:
 *   - Application
 * entities:
 *   - entity_name: Application
 *     access_mode: write
 *   - entity_name: JobOffer
 *     access_mode: read
 *   - entity_name: Education
 *     access_mode: read
 */

/**
 * @Operation
 * name: createEducation
 * integrity: low
 * frequency: 4
 * forced_entities:
 *   - Education
 * entities:
 *   - entity_name: Education
 *     access_mode: write
 */

/**
 * @Operation
 * name: createExperience
 * integrity: low
 * frequency: 3
 * forced_entities:
 *   - Experience
 * entities:
 *   - entity_name: Experience
 *     access_mode: write
 */

/**
 * @Operation
 * name: createLanguage
 * integrity: low
 * frequency: 3
 * forced_entities:
 *   - Language
 * entities:
 *   - entity_name: Language
 *     access_mode: write
 *   - entity_name: LanguageLevel
 *     access_mode: read
 *   - entity_name: UserHasLanguage
 *     access_mode: write
 */

/**
 * @Operation
 * name: createSkill
 * integrity: low
 * frequency: 3
 * forced_entities:
 *   - Skill
 * entities:
 *   - entity_name: Skill
 *     access_mode: read
 *   - entity_name: SkillLevel
 *     access_mode: read
 *   - entity_name: UserHasSkill
 *     access_mode: write
 */

/**
 * @Operation
 * name: deleteEducation
 * integrity: low
 * frequency: 3
 * forced_entities:
 *   - Education
 * entities:
 *   - entity_name: Education
 *     access_mode: write
 */

/**
 * @Operation
 * name: deleteExperience
 * integrity: low
 * frequency: 3
 * forced_entities:
 *   - Experience
 * entities:
 *   - entity_name: Experience
 *     access_mode: write
 */

/**
 * @Operation
 * name: deleteInterview
 * integrity: low
 * frequency: 5
 * forced_entities:
 *   - Interview
 * entities:
 *   - entity_name: Interview
 *     access_mode: write
 *   - entity_name: Application
 *     access_mode: read
 */

/**
 * @Operation
 * name: deleteLanguage
 * integrity: low
 * frequency: 3
 * forced_entities:
 *   - Language
 * entities:
 *   - entity_name: UserHasLanguage
 *     access_mode: write
 */

/**
 * @Operation
 * name: deleteSkill
 * integrity: low
 * frequency: 3
 * forced_entities:
 *   - Skill
 * entities:
 *   - entity_name: UserHasSkill
 *     access_mode: write
 */

/**
 * @Operation
 * name: deleteStory
 * integrity: low
 * frequency: 5
 * forced_entities:
 *   - Application
 * entities:
 *   - entity_name: Application
 *     access_mode: write
 */

/**
 * @Operation
 * name: deleteUser
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   - User
 * entities:
 *   - entity_name: User
 *     access_mode: write
 */

/**
 * @Operation
 * name: employerRetrieveCurriculum
 * integrity: low
 * frequency: 7
 * forced_entities:
 *   - User
 * entities:
 *   - entity_name: User
 *     access_mode: read
 *   - entity_name: Education
 *     access_mode: read
 *   - entity_name: StudyTag
 *     access_mode: read
 *   - entity_name: Skill
 *     access_mode: read
 *   - entity_name: Language
 *     access_mode: read
 *   - entity_name: UserHasSkill
 *     access_mode: read
 *   - entity_name: UserHasLanguage
 *     access_mode: read
 *   - entity_name: LanguageLevel
 *     access_mode: read
 *   - entity_name: SkillLevel
 *     access_mode: read
 */

/**
 * @Operation
 * name: employerRetrieveUserInfo
 * integrity: low
 * frequency: 6
 * forced_entities:
 *   - User
 * entities:
 *   - entity_name: User
 *     access_mode: read
 *   - entity_name: Education
 *     access_mode: read
 *   - entity_name: StudyTag
 *     access_mode: read
 *   - entity_name: Skill
 *     access_mode: read
 *   - entity_name: Language
 *     access_mode: read
 *   - entity_name: UserHasSkill
 *     access_mode: read
 *   - entity_name: UserHasLanguage
 *     access_mode: read
 *   - entity_name: LanguageLevel
 *     access_mode: read
 *   - entity_name: SkillLevel
 *     access_mode: read
 */

/**
 * @Operation
 * name: eventCheckIn
 * integrity: low
 * frequency: 7
 * forced_entities:
 *   - CheckIn
 * entities:
 *   - entity_name: CheckIn
 *     access_mode: write
 *   - entity_name: Event
 *     access_mode: read
 *   - entity_name: Education
 *     access_mode: read
 */

/**
 * @Operation
 * name: participateWebinar
 * integrity: low
 * frequency: 5
 * forced_entities:
 *   - WebinarParticipation
 * entities:
 *   - entity_name: WebinarParticipation
 *     access_mode: write
 *   - entity_name: Education
 *     access_mode: read
 *   - entity_name: Webinar
 *     access_mode: read
 */

/**
 * @Operation
 * name: registerToCareerDay
 * integrity: low
 * frequency: 3
 * forced_entities:
 *   - CareerDay
 * entities:
 *   - entity_name: CareerDay
 *     access_mode: read
 *   - entity_name: CareerDayRegistration
 *     access_mode: write
 *   - entity_name: Education
 *     access_mode: read
 */

/**
 * @Operation
 * name: retrieveActivities
 * integrity: low
 * frequency: 4
 * forced_entities:
 *   - User
 * entities:
 *   - entity_name: User
 *     access_mode: read
 *   - entity_name: Application
 *     access_mode: read
 *   - entity_name: JobOffer
 *     access_mode: read
 *   - entity_name: Content
 *     access_mode: read
 *   - entity_name: Type
 *     access_mode: read
 *   - entity_name: City
 *     access_mode: read
 *   - entity_name: WebinarParticipation
 *     access_mode: read
 *   - entity_name: CheckIn
 *     access_mode: read
 *   - entity_name: Webinar
 *     access_mode: read
 *   - entity_name: Event
 *     access_mode: read
 */

/**
 * @Operation
 * name: retrieveApplication
 * integrity: high
 * frequency: 6
 * forced_entities:
 *   - Application
 * entities:
 *   - entity_name: JobOffer
 *     access_mode: read
 *   - entity_name: Application
 *     access_mode: read
 */

/**
 * @Operation
 * name: retrieveCompanies
 * integrity: low
 * frequency: 5
 * forced_entities:
 *   - User
 * entities:
 *   - entity_name: User
 *     access_mode: read
 *   - entity_name: Profile
 *     access_mode: read
 *   - entity_name: Industry
 *     access_mode: read
 */

/**
 * @Operation
 * name: retrieveCurrentUniversityInfo
 * integrity: low
 * frequency: 10
 * forced_entities:
 *   - User
 * entities:
 *   - entity_name: User
 *     access_mode: read
 *   - entity_name: Education
 *     access_mode: read
 *   - entity_name: Institute
 *     access_mode: read
 *   - entity_name: StudyTag
 *     access_mode: read
 */

/**
 * @Operation
 * name: retrieveCurriculum
 * integrity: low
 * frequency: 5
 * forced_entities:
 *   - User
 * entities:
 *   - entity_name: User
 *     access_mode: read
 *   - entity_name: Education
 *     access_mode: read
 *   - entity_name: StudyTag
 *     access_mode: read
 *   - entity_name: Skill
 *     access_mode: read
 *   - entity_name: Language
 *     access_mode: read
 *   - entity_name: UserHasSkill
 *     access_mode: read
 *   - entity_name: UserHasLanguage
 *     access_mode: read
 *   - entity_name: LanguageLevel
 *     access_mode: read
 *   - entity_name: SkillLevel
 *     access_mode: read
 */

/**
 * @Operation
 * name: retrieveEmployerInfo
 * integrity: low
 * frequency: 5
 * forced_entities:
 *   - User
 * entities:
 *   - entity_name: User
 *     access_mode: read
 *   - entity_name: Profile
 *     access_mode: read
 *   - entity_name: Education
 *     access_mode: read
 */

/**
 * @Operation
 * name: retrieveEmployerJobOffers
 * integrity: low
 * frequency: 8
 * forced_entities:
 *   - JobOffer
 * entities:
 *   - entity_name: JobOffer
 *     access_mode: read
 *   - entity_name: User
 *     access_mode: read
 *   - entity_name: Profile
 *     access_mode: read
 *   - entity_name: Stream
 *     access_mode: read
 *   - entity_name: City
 *     access_mode: read
 *   - entity_name: Type
 *     access_mode: read
 */

/**
 * @Operation
 * name: retrieveEmployerPosts
 * integrity: low
 * frequency: 8
 * forced_entities:
 *   - Post
 * entities:
 *   - entity_name: Post
 *     access_mode: read
 *   - entity_name: User
 *     access_mode: read
 *   - entity_name: Profile
 *     access_mode: read
 *   - entity_name: Stream
 *     access_mode: read
 *   - entity_name: Content
 *     access_mode: read
 */

/**
 * @Operation
 * name: retrieveEmployerWebinars
 * integrity: low
 * frequency: 8
 * forced_entities:
 *   - Webinar
 * entities:
 *   - entity_name: Webinar
 *     access_mode: read
 *   - entity_name: User
 *     access_mode: read
 *   - entity_name: Profile
 *     access_mode: read
 *   - entity_name: Stream
 *     access_mode: read
 *   - entity_name: Content
 *     access_mode: read
 */

/**
 * @Operation
 * name: retrieveEventDetail
 * integrity: low
 * frequency: 5
 * forced_entities:
 *   - Event
 * entities:
 *   - entity_name: Event
 *     access_mode: read
 *   - entity_name: JobOffer
 *     access_mode: read
 */

/**
 * @Operation
 * name: retrieveExperienceTypes
 * integrity: low
 * frequency: 5
 * forced_entities:
 *   - ExperienceType
 * entities:
 *   - entity_name: ExperienceType
 *     access_mode: read
 */

/**
 * @Operation
 * name: retrieveInstitutes
 * integrity: low
 * frequency: 8
 * forced_entities:
 *   - Institute
 * entities:
 *   - entity_name: Institute
 *     access_mode: read
 *   - entity_name: City
 *     access_mode: read
 *   - entity_name: Country
 *     access_mode: read
 */

/**
 * @Operation
 * name: retrieveJobOfferDetail
 * integrity: low
 * frequency: 8
 * forced_entities:
 *   - JobOffer
 * entities:
 *   - entity_name: JobOffer
 *     access_mode: read
 *   - entity_name: City
 *     access_mode: read
 *   - entity_name: Sector
 *     access_mode: read
 *   - entity_name: Industry
 *     access_mode: read
 *   - entity_name: Type
 *     access_mode: read
 *   - entity_name: User
 *     access_mode: read
 */

/**
 * @Operation
 * name: retrieveLanguageLevels
 * integrity: low
 * frequency: 5
 * forced_entities:
 *   - LanguageLevel
 * entities:
 *   - entity_name: LanguageLevel
 *     access_mode: read
 */

/**
 * @Operation
 * name: retrieveLanguages
 * integrity: low
 * frequency: 5
 * forced_entities:
 *   - Language
 * entities:
 *   - entity_name: Language
 *     access_mode: read
 */

/**
 * @Operation
 * name: retrievePostDetail
 * integrity: low
 * frequency: 6
 * forced_entities:
 *   - Post
 * entities:
 *   - entity_name: Post
 *     access_mode: read
 *   - entity_name: JobOffer
 *     access_mode: read
 *   - entity_name: City
 *     access_mode: read
 *   - entity_name: Type
 *     access_mode: read
 *   - entity_name: Stream
 *     access_mode: read
 *   - entity_name: Content
 *     access_mode: read
 */

/**
 * @Operation
 * name: retrieveQualifications
 * integrity: low
 * frequency: 8
 * forced_entities:
 *   - Qualification
 * entities:
 *   - entity_name: Qualification
 *     access_mode: read
 *   - entity_name: Institute
 *     access_mode: read
 */

/**
 * @Operation
 * name: retrieveSkillLevels
 * integrity: low
 * frequency: 5
 * forced_entities:
 *   - SkillLevel
 * entities:
 *   - entity_name: SkillLevel
 *     access_mode: read
 */

/**
 * @Operation
 * name: retrieveSkills
 * integrity: low
 * frequency: 5
 * forced_entities:
 *   - Skill
 * entities:
 *   - entity_name: Skill
 *     access_mode: read
 */

/**
 * @Operation
 * name: retrieveStoryVideo
 * integrity: low
 * frequency: 2
 * forced_entities:
 *   - Application
 * entities:
 *   - entity_name: Application
 *     access_mode: read
 *   - entity_name: EmployerHasOperator
 *     access_mode: read
 */

/**
 * @Operation
 * name: retrieveStreamBySlug
 * integrity: low
 * frequency: 5
 * forced_entities:
 *   - Stream
 * entities:
 *   - entity_name: Stream
 *     access_mode: read
 *   - entity_name: JobOffer
 *     access_mode: read
 *   - entity_name: City
 *     access_mode: read
 *   - entity_name: Type
 *     access_mode: read
 *   - entity_name: Content
 *     access_mode: read
 *   - entity_name: Post
 *     access_mode: read
 *   - entity_name: Webinar
 *     access_mode: read
 *   - entity_name: CommunityArticle
 *     access_mode: read
 */

/**
 * @Operation
 * name: retrieveStreamDetail
 * integrity: low
 * frequency: 5
 * forced_entities:
 *   - Stream
 * entities:
 *   - entity_name: Stream
 *     access_mode: read
 *   - entity_name: JobOffer
 *     access_mode: read
 *   - entity_name: City
 *     access_mode: read
 *   - entity_name: Type
 *     access_mode: read
 *   - entity_name: Content
 *     access_mode: read
 *   - entity_name: Post
 *     access_mode: read
 *   - entity_name: Webinar
 *     access_mode: read
 *   - entity_name: CommunityArticle
 *     access_mode: read
 */

/**
 * @Operation
 * name: retrieveStreamsHome
 * integrity: low
 * frequency: 10
 * forced_entities:
 *   - Stream
 * entities:
 *   - entity_name: Stream
 *     access_mode: read
 *   - entity_name: JobOffer
 *     access_mode: read
 *   - entity_name: City
 *     access_mode: read
 *   - entity_name: Type
 *     access_mode: read
 *   - entity_name: Content
 *     access_mode: read
 *   - entity_name: Post
 *     access_mode: read
 *   - entity_name: Webinar
 *     access_mode: read
 *   - entity_name: CommunityArticle
 *     access_mode: read
 */

/**
 * @Operation
 * name: retrieveStudyTags
 * integrity: low
 * frequency: 8
 * forced_entities:
 *   - StudyTag
 * entities:
 *   - entity_name: StudyTag
 *     access_mode: read
 */

/**
 * @Operation
 * name: retrieveVotes
 * integrity: low
 * frequency: 8
 * forced_entities:
 *   - Vote
 * entities:
 *   - entity_name: Vote
 *     access_mode: read
 *   - entity_name: Qualification
 *     access_mode: read
 */

/**
 * @Operation
 * name: retrieveWebinarDetail
 * integrity: low
 * frequency: 6
 * forced_entities:
 *   - Webinar
 * entities:
 *   - entity_name: Webinar
 *     access_mode: read
 *   - entity_name: Content
 *     access_mode: read
 *   - entity_name: User
 *     access_mode: read
 */

/**
 * @Operation
 * name: retrieveWebinarParticipation
 * integrity: low
 * frequency: 6
 * forced_entities:
 *   - WebinarParticipation
 * entities:
 *   - entity_name: WebinarParticipation
 *     access_mode: read
 *   - entity_name: Webinar
 *     access_mode: read
 */

/**
 * @Operation
 * name: scheduleInterview
 * integrity: low
 * frequency: 5
 * forced_entities:
 *   - Interview
 * entities:
 *   - entity_name: Interview
 *     access_mode: write
 *   - entity_name: JobOffer
 *     access_mode: read
 *   - entity_name: Application
 *     access_mode: read
 */

/**
 * @Operation
 * name: startApply
 * integrity: low
 * frequency: 8
 * forced_entities:
 *   - Application
 * entities:
 *   - entity_name: Application
 *     access_mode: write
 *   - entity_name: JobOffer
 *     access_mode: read
 */

/**
 * @Operation
 * name: updateContacts
 * integrity: low
 * frequency: 2
 * forced_entities:
 *   - User
 * entities:
 *   - entity_name: User
 *     access_mode: write
 */

/**
 * @Operation
 * name: updateEducation
 * integrity: low
 * frequency: 3
 * forced_entities:
 *   - Education
 * entities:
 *   - entity_name: Education
 *     access_mode: write
 */

/**
 * @Operation
 * name: updateExperience
 * integrity: low
 * frequency: 3
 * forced_entities:
 *   - Experience
 * entities:
 *   - entity_name: Experience
 *     access_mode: write
 */

/**
 * @Operation
 * name: updateExperienceOrder
 * integrity: low
 * frequency: 2
 * forced_entities:
 *   - Experience
 * entities:
 *   - entity_name: Experience
 *     access_mode: write
 */

/**
 * @Operation
 * name: updateLanguageOrder
 * integrity: low
 * frequency: 3
 * forced_entities:
 *   - Language
 * entities:
 *   - entity_name: UserHasLanguage
 *     access_mode: write
 */

/**
 * @Operation
 * name: updateOrderEducation
 * integrity: low
 * frequency: 2
 * forced_entities:
 *   - Education
 * entities:
 *   - entity_name: Education
 *     access_mode: write
 */

/**
 * @Operation
 * name: updateProfile
 * integrity: low
 * frequency: 3
 * forced_entities:
 *   - User
 * entities:
 *   - entity_name: User
 *     access_mode: write
 */

/**
 * @Operation
 * name: updateSkillOrder
 * integrity: low
 * frequency: 3
 * forced_entities:
 *   - Skill
 * entities:
 *   - entity_name: UserHasSkill
 *     access_mode: write
 */

/**
 * @Operation
 * name: updateUserProfile
 * integrity: low
 * frequency: 2
 * forced_entities:
 *   - User
 * entities:
 *   - entity_name: User
 *     access_mode: write
 */

/**
 * @Operation
 * name: uploadCV
 * integrity: low
 * frequency: 3
 * forced_entities:
 *   - Event
 * entities:
 *   - entity_name: CheckIn
 *     access_mode: write
 *   - entity_name: User
 *     access_mode: read
 */

/**
 * @Operation
 * name: uploadStory
 * integrity: low
 * frequency: 5
 * forced_entities:
 *   - Application
 * entities:
 *   - entity_name: Application
 *     access_mode: write
 *   - entity_name: JobOffer
 *     access_mode: read
 */

/**
 * @Operation
 * name: usersMe
 * integrity: low
 * frequency: 10
 * forced_entities:
 *   - User
 * entities:
 *   - entity_name: User
 *     access_mode: read
 *   - entity_name: Education
 *     access_mode: read
 *   - entity_name: StudyTag
 *     access_mode: read
 *   - entity_name: Skill
 *     access_mode: read
 *   - entity_name: Language
 *     access_mode: read
 *   - entity_name: UserHasSkill
 *     access_mode: read
 *   - entity_name: UserHasLanguage
 *     access_mode: read
 *   - entity_name: LanguageLevel
 *     access_mode: read
 *   - entity_name: SkillLevel
 *     access_mode: read
 */

/**
 * @Operation
 * name: webinarOffline
 * integrity: low
 * frequency: 3
 * forced_entities:
 *   - WebinarParticipation
 * entities:
 *   - entity_name: WebinarParticipation
 *     access_mode: write
 *   - entity_name: Education
 *     access_mode: read
 *   - entity_name: Webinar
 *     access_mode: read
 */

/**
 * @Operation
 * name: webinarRegistration
 * integrity: low
 * frequency: 5
 * forced_entities:
 *   - WebinarParticipation
 * entities:
 *   - entity_name: WebinarParticipation
 *     access_mode: write
 *   - entity_name: Education
 *     access_mode: read
 *   - entity_name: Webinar
 *     access_mode: read
 */

