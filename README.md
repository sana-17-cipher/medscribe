
# MedScribe AI

MedScribe AI is an AI-powered medical speech recognition and documentation system designed to streamline clinical workflows. The system enables healthcare professionals to record or upload voice input and automatically generate structured medical reports using speech-to-text and natural language processing techniques.

## Overview

Medical documentation is time-consuming and often disrupts clinical efficiency. MedScribe AI addresses this problem by converting spoken medical notes into structured, readable reports. The system supports multiple documentation types including consultations, surgical notes, pre-operative and post-operative records, anesthesia records, and nursing notes.

The application operates locally, ensuring privacy and reducing dependency on external services.

## Features

Speech to text transcription using OpenAI Whisper running locally
Automatic extraction of medical entities and structured report generation
Support for multiple note types including consultation and surgical documentation
PDF report generation for clinical use
Patient and session history tracking
Browser-based interface for recording and uploading audio
Offline processing for improved privacy and reliability

## Technology Stack

Speech to Text: OpenAI Whisper
Natural Language Processing: spaCy with rule-based extraction
Backend: Flask (Python)
Database: SQLite using SQLAlchemy ORM
Frontend: HTML, CSS, JavaScript
PDF Generation: ReportLab
Audio Processing: pydub and sounddevice

## System Architecture

The system follows a simple pipeline:

Audio Input
Audio is recorded or uploaded via the frontend interface

Transcription
The backend processes the audio using Whisper to generate raw text

NLP Processing
The transcription is analyzed using spaCy and custom rules to extract structured medical information

Report Generation
Structured data is formatted into a readable report and optionally exported as a PDF

Storage
All sessions, transcriptions, and reports are stored in a local database

## Project Structure

backend
Contains Flask API, Whisper integration, NLP parser, report builder, and database models

frontend
Contains user interface files including dashboard, recording functionality, and export features

tests
Includes unit tests and sample inputs for validation

## API Endpoints

POST /transcribe
Accepts audio input and returns transcribed text

POST /parse
Processes transcription and returns structured medical data

GET /export/<id>
Generates and downloads a PDF report

## Database Schema

Patients
Stores patient demographic information

Sessions
Represents individual medical interactions

Transcriptions
Stores raw text generated from audio

Reports
Stores structured output and PDF references

Relationships follow a one-to-many structure from patients to sessions and sessions to reports and transcriptions.

## Setup Instructions

Clone the repository and navigate to the project directory

Install dependencies using requirements.txt

Run the backend server using Python

Open the frontend dashboard in a browser

Record or upload audio to generate reports

## Usage

Start the backend server
Open the dashboard interface
Record or upload an audio file
Wait for transcription and processing
View structured output in the interface
Export the report as a PDF if required

## Testing

Run unit tests for the NLP parser and API endpoints using pytest

Manual testing can be performed by uploading sample audio files and verifying transcription accuracy and report generation

## Privacy and Compliance

This project is designed for local use and does not transmit data externally. For real-world deployment involving patient data, the system must be hosted on compliant infrastructure and implement encryption for data at rest and in transit.

## Future Enhancements

Integration with electronic health record systems
Improved medical entity recognition using advanced models
Real-time transcription support
Multi-user authentication and role-based access
Cloud deployment for hospital-scale usage

## License

This project is intended for educational and research purposes.
