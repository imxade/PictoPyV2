
import os
import sqlite3
from sqlite3 import IntegrityError
from typing import Dict, List, Generator, Tuple
from utils.fs import genHash, isImg, imgPaths, homeDir, detectFileWithHash, deleteFile
from utils.db import connectDB, createTable, executeQuery, closeConnection, groupByClass, hashExist, hideByClass, unhideByClass, deleteFromDB, deleteByClass, toggleVisibility
from utils.createDB import  createSchema, classesExist
from yolov8 import detectClasslass
from flask import Flask, render_template, send_file, request
from markupsafe import escape


def processImgs(conn: sqlite3.Connection, files: Generator[str, None, None]) -> None:
    """
    Processes images by extracting their hash values, detecting their classes, and storing them in the database.

    Args:
        conn: The database connection object.
        files: A generator of file paths.
    """

    for file in files:
        imgHash = genHash(file)
        if hashExist(conn, imgHash):
            continue
        try:
            imgClass = detectClasslass(file)
            _, imageID = executeQuery(conn, f"INSERT INTO MEDIA(hash, path, hidden) VALUES('{imgHash}', '{file}', 0)", 1)

            for className in imgClass:
                try:
                    _, classID = executeQuery(conn, f"INSERT INTO CLASS(class) VALUES('{className}')", 1)
                except IntegrityError:
                    classID = executeQuery(conn, f"SELECT classID FROM CLASS WHERE class = '{className}'")[0][0]
                
                executeQuery(conn, f"INSERT OR IGNORE INTO JUNCTION(imageID, classID) VALUES('{imageID}', '{classID}')")

        except IntegrityError:
            executeQuery(conn, f"UPDATE MEDIA SET path = '{file}' WHERE hash = '{imgHash}'")


#NN
def fileByClass(conn: sqlite3.Connection, files: Generator[str, None, None], tableID: str) -> Dict[str, List[str]]:
    rows = executeQuery(conn, f"SELECT imageClass, hash FROM {tableID}")
    classDict = {}
    for row in rows:
        imageClass, hashValue = row
        if imageClass not in classDict:
            classDict[imageClass] = []
        filePath = detectFileWithHash(files, hashValue)
        if filePath:
            classDict[imageClass].append(filePath)
    return classDict

def classifyPath() -> Dict[str, Tuple[str]]:
    """
    Classify images in the home directory and store the results in the database.

    Returns:
        Dict[str, Tuple[str]]: Dictionary mapping class names to lists of file paths.
    """
    dbPath = os.path.join(homeDir(), ".pictopy.db")
    conn = connectDB(dbPath)
    createSchema(conn)

    files = imgPaths(homeDir())
    processImgs(conn, files)

    # Re-create the generator since it would be exhausted
    files = imgPaths(homeDir())  
    result = groupByClass(conn)

    closeConnection(conn)

    return result

# periodically run the object detection function and compare it with DB (TBI)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', classDict=classifyPath())

@app.route('/media/<path:filename>')
def media(filename):
    return send_file(f"/{escape(filename)}")

@app.route('/operate', methods=['POST'])
def operate():
    action = request.form['action']
    selectedImages = request.form.getlist('selectedImages')

    if action == 'delete':
        return f"Deleting images: {selectedImages}"
    elif action == 'hide':
        return f"Hiding images: {selectedImages}"
    else:
        return "Unknown action"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
