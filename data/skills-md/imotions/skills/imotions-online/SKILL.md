---
name: "imotions-online"
description: "Access data in an iMotions Online study. Use when working with building a study, analyzing the results or comparing segments in a study."
---

# iMotions Online

iMotions Online is a platform for building and running multimodal consumer insights, experimental psychology and human factors studies on the web.
A study contains a series of stimuli that are shown to respondents while data about their behavior is collected.

The iMotions Online CLI tool gives access to the data in a study. It is located in the same folder as this skill.
Depending on how the skill was installed, the folder contains either `aimotions.exe` or `aimotions.js`.
Check which one is present, then run the executable directly with `aimotions.exe` or the Javascript file with `node aimotions.js`.

If the user is not authenticated, the tool will automatically start the auth process.
This will show a URL that you need to tell the user to open in their browser to accept the authentication request.
Once the user has accepted this, you can run the command again.

The commands call various REST API endpoints to get the data. Do not attempt to call them yourself directly.
Some of the outputs include full URLs to images or gzipped JSON files. These URLs can be fetched without authentication, so you can use them to get the data you need.

iMotions Lab is the Windows desktop version of iMotions. Only data from iMotions Online is accessible here.

## List studies

Get a list of all the studies the user has access to.

`aimotions list-studies`

## Study overview

Gets an overview of the stimuli, sensors, respondents and segments in a study.
Run it with the name of the study in double quotes.

`aimotions study-overview "Study name"`

## Segment details

A study contains a number of segments that group individual respondents together. These can then be used to compare data from different segments.
The "All Respondents" segment is always present and contains every respondent in the study.
Gets the details of a segment, including summary metrics, survey answers, AOI metrics and links to aggregated data.
Run it with the name of the study followed by the name of the segment, both in double quotes.

`aimotions segment-details "Study name" "Segment name"`

To include all summary metrics instead of only the most important ones, add `--all-metrics`.

## Stimulus details

A study contains a number of stimuli that are shown to respondents.
Gets the details of a stimulus, including annotations.
Run it with the name of the study followed by the name of the stimulus, both in double quotes.

`aimotions stimulus-details "Study name" "Stimulus name"`

## Respondent details

A study contains a number of respondents that have taken part in the study.
Gets the details of a respondent, including variables, survey answers and links to raw data.
Run it with the name of the study followed by the label of the respondent, both in double quotes.

`aimotions respondent-details "Study name" "Respondent label"`

## Stimulus segment details

Gets the data for a single stimulus and segment combination. Use this when the user asks about how a segment responded to a specific stimulus.
It includes the overall summary metrics for the stimulus and segment, and per-annotation summary metrics when annotations are available.
For videos with video segment annotations, this can describe the metrics by scene.
For stimuli in general, it can describe the annotated intervals and their metrics when the stimulus has annotations and signal data.
Run it with the name of the study, the name of the stimulus, and the name of the segment, all in double quotes.

`aimotions stimulus-segment-details "Study name" "Stimulus name" "Segment name"`

To focus on one annotation, add `--annotation "Annotation name"`.
To show metrics for each individual interval instead of aggregated annotation metrics, add `--individual-intervals`.
To include all summary metrics instead of only the most important ones, add `--all-metrics`.

## CSV exports

The following commands output CSV instead of Markdown, to make the data easy to process programmatically.
Like the other commands, run them with the study, stimulus, segment and respondent names in double quotes.
The output can be large, so prefer writing it to a file with `--output file.csv` and analyzing the file with a script, instead of reading the whole output.

### Respondents

Lists every respondent in the study with their details: label, age, gender, flow, start and end times, variables and survey answers. One row per respondent.

`aimotions list-respondents-csv "Study name" --output respondents.csv`

To add columns with the URL of each respondent's raw data for each stimulus, add `--raw-data-urls`.
The URLs point to gzipped JSON files that can be fetched without authentication. See respondent-details for an explanation of the fields.

To track progress while data collection is running, add `--progress`. This makes it also include respondents that have not completed the study.
The "State" column shows "In progress" (still taking the study), "Processing" (finished, data still being processed), "Completed", "Abandoned" (left the study partway through) or "Processing error".
The "Progress" column shows how far along the in progress respondents are (setup step, which stimulus they are viewing, or uploading), and where the abandoned respondents stopped.
The "Estimated end time" column estimates when the in progress respondents will finish, based on the typical duration of the respondents who have already finished. It is empty when no respondents have finished yet.
The "Last heartbeat" column shows when an in progress respondent was last active, which is useful for spotting stalled sessions that will eventually count as abandoned.

### Stimulus metrics

Lists the summary metrics of a study, with one row per stimulus, segment and signal combination and columns for the mean, standard deviation, variance and count.
Use this instead of many segment-details or stimulus-segment-details calls when comparing metrics across stimuli or segments, or when doing statistical analysis.

`aimotions stimulus-metrics-csv "Study name" --output metrics.csv`

To only include one stimulus, add `--stimulus "Stimulus name"`. To only include one segment, add `--segment "Segment name"`.

### AOI metrics

Lists the eye tracking metrics of every AOI in a study, with one row per AOI and segment combination and one column per metric, such as time to first fixation, dwell time and respondent ratio.
This includes all the available metrics, unlike segment-details which only shows the most important ones.
Use this when comparing AOIs across stimuli or segments, or when doing statistical analysis.

`aimotions aoi-metrics-csv "Study name" --output aoi-metrics.csv`

To only include the AOIs on one stimulus, add `--stimulus "Stimulus name"`. To only include one segment, add `--segment "Segment name"`.

### Annotation metrics

Lists the metrics of every annotation interval in a study, with one row per interval, stimulus and segment combination and one column per signal.
This is the same data as the annotation metrics in stimulus-segment-details, but for the whole study at once, so use it for scene-by-scene analysis of a video across segments instead of calling stimulus-segment-details for each stimulus.

`aimotions annotation-metrics-csv "Study name" --output annotation-metrics.csv`

To narrow it down, add `--stimulus "Stimulus name"`, `--segment "Segment name"` or `--annotation "Annotation name"`.
To get one row per annotation with the metrics averaged over all of its intervals, instead of one row per interval, add `--aggregated-intervals`.
The metrics are calculated from the facial expression signals, so they are only available for stimuli where respondents have processed webcam data.

### Signal timeline

Exports the recorded signal time series for one stimulus, with one row per timestamp and one column per signal, such as the facial expression signals, gaze coordinates, fixations and respiration.
This is the raw binned data behind the summary metrics, so use it when the aggregated metrics are not enough, for example to see how a signal develops over time or to run your own statistics.
Run it with either `--segment` to get the aggregated timeline of a segment or `--respondent` to get the individual timeline of a respondent.

`aimotions signal-timeline-csv "Study name" "Stimulus name" --segment "Segment name" --output timeline.csv`

`aimotions signal-timeline-csv "Study name" "Stimulus name" --respondent "Respondent label" --output timeline.csv`

This output is very large, so always write it to a file with `--output`.
The timestamps are milliseconds from the start of the stimulus exposure. Sensors are sampled at different rates, so a cell is empty when that signal has no value at that timestamp.

### Fixations and gaze points

Exports the eye tracking data of the individual respondents for one stimulus, so you can do your own heatmaps, scanpaths or AOI hit testing without having to fetch and reshape the raw JSON data files.

`aimotions fixations-csv "Study name" "Stimulus name" --output fixations.csv` gives one row per fixation with the respondent label, start and end time in milliseconds, and the x and y coordinate of the fixation.

`aimotions gazes-csv "Study name" "Stimulus name" --output gazes.csv` gives one row per gaze point with the respondent label, timestamp in milliseconds and the x and y coordinate.

This output is very large, so always write it to a file with `--output`.
To only include one respondent, for example to look at a single scanpath, add `--respondent "Respondent label"`.
The coordinates are normalized to a 1920x1080 coordinate system regardless of the actual size of the stimulus, so scale them to the stimulus size from stimulus-details when comparing them to something else. They can fall outside that range when the respondent looked away from the stimulus.
Gaze points where the eye tracking lost the respondent are left out, and several gaze points can share a timestamp.

## Create new segment

Create a new segment by specifying the labels of the respondents that should be included.
It will take a few minutes to process data for the new segment.  
Run it with the name of the study, the name of the segment, and the labels of the respondents, all in double quotes.

`aimotions create-segment "Study name" "Segment name" "Respondent label 1" "Respondent label 2"...`

## Edit segment

Rename a segment or change which respondents it contains. The "All Respondents" segment cannot be changed.
Run it with the name of the study and the name of the segment in double quotes, followed by the changes to make.

`aimotions edit-segment "Study name" "Segment name" --name "New name" --add-respondents "Respondent label 1,Respondent label 2" --remove-respondents "Respondent label 3"`

Only the specified options are changed. When the respondents change, it will take a few minutes to reprocess data for the segment.

## Add annotation interval

An annotation groups together a series of named time intervals (also called fragments) on the stimuli of a study.
Add an interval to an annotation on a stimulus. If no annotation with that name exists in the study, it is created automatically.
The start and end times are in milliseconds from the start of the stimulus, and intervals of the same annotation cannot overlap on the same stimulus.
Run it with the name of the study, the name of the annotation and the name of the stimulus in double quotes, followed by the start and end times in milliseconds.

`aimotions add-annotation-fragment "Study name" "Annotation name" "Stimulus name" 1000 5000`

To give the interval a text label, add `--text "Label"`.
To attach the interval to a single respondent instead of the whole stimulus, add `--respondent "Respondent label"`.
The automatically generated "Video Segments" annotations cannot be changed.

## Edit annotation interval

Change the time range or text label of an existing annotation interval.
The interval is identified by its current start time in milliseconds, which can be found with the stimulus details command.

`aimotions edit-annotation-fragment "Study name" "Annotation name" "Stimulus name" 1000 --start-ms 1500 --end-ms 6000 --text "New label"`

Only the specified options are changed, so for example the end time can be changed on its own.

## Delete annotation interval

Delete an existing annotation interval.
The interval is identified by its current start time in milliseconds, which can be found with the stimulus details command.
If it was the annotation's last interval, the annotation itself is also deleted.

`aimotions delete-annotation-fragment "Study name" "Annotation name" "Stimulus name" 1000`

## List AOIs

An area of interest (AOI) marks an area on a stimulus, which creates eye tracking metrics based on when respondents look at it, such as time to first fixation and dwell time.
Lists the AOIs in a study with their positions and sizes.

`aimotions list-aois "Study name"`

To only show the AOIs on one stimulus, add `--stimulus "Stimulus name"`.

## Create, edit and delete AOIs

Instructions for creating, editing and deleting AOIs, including how to specify their shapes and how to size them for webcam eye tracking accuracy, are in [aoi-editing.md](./aoi-editing.md).
Read it before making any AOI changes.

## Add note

Add a note to the study or an item in it. The notes are shown to the user in the web interface, so use them to record interesting 
discoveries you make when examining the data, or to explain why you made a change (e.g. why you created a segment or an annotation interval).
It is **very important** to keep notes short and factual, and only add information not otherwise available.
Check the existing notes with list-notes first so you don't repeat them. Don't narrate routine steps. Don't duplicate information about the study/stimulus/segment.

`aimotions add-note "Study name" "The note text"`

Without options the note is attached to the study itself. To attach it to a specific item, add one of:
- `--segment "Segment name"`
- `--respondent "Respondent label"`
- `--stimulus "Stimulus name"`
- `--annotation "Annotation name" --stimulus "Stimulus name" --start-ms 1000` for an annotation interval, identified by its start time like in edit-annotation-fragment.

## List notes

List the notes attached to a study and the items in it, including each note's ID.

`aimotions list-notes "Study name"`

## Delete note

Delete a note, identified by the ID shown by list-notes. Only do this when a note is wrong or outdated.

`aimotions delete-note "Study name" "Note ID"`

## Search the iMotions Help Center

The iMotions Help Center contains documentation about how to use the product. Users can access it on [https://help.imotions.com](https://help.imotions.com).
Search it when the user asks how to do something in iMotions, or when you need product knowledge beyond what is provided here.
Note that some of the articles apply to iMotions Lab, the Windows desktop version, which is not relevant here.

`aimotions search-help "search phrase"`

## Read a Help Center article

Read the full content of a Help Center article, using the article ID from the search results.
When answering the user based on an article, include the article URL so they can read more.

`aimotions help-article "article-id"`

# Building and editing studies

Studies can also be built and edited: creating a new study from scratch, and creating and changing its flows, blocks and stimuli, as long as it has not started data collection yet.
The account also has a media library of images and videos that can be reused as stimuli across studies.
Commands for this, and a description of how flows and blocks work, are in [study-editing.md](./study-editing.md). Read it before creating a study or changing the design of one.
It also describes how to verify a built study by previewing its flows in a browser.

# References

References to articles and academic papers that explain eye tracking and facial expressions, and how to conduct research with them are available in [articles.md](./articles.md).
