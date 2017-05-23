from pymongo import MongoClient  # For connecting to MongoDB


def search_exp(entries):
    """
    Locates the metadata for experiments from an user defined search field and search term
    :param entries: contains the search field and the corresponding search term
    :return: metadata (list): a list of dictionaries containing the metadata for the found experiments
    """
    # This assumes only a single field:term pair
    field = str()
    term = str()

    for entry in entries:
        field = entry[0].get()
        term = entry[1].get()

    # Need to search across the metadata and allow for selection of hits
    # Place those hits into separate Meta instances
    metadata = []
    client = MongoClient()
    db = client['nodbase']
    cursor = db['meta'].find({field: term})

    for document in cursor:
        metadata.append(document)

    return metadata


def search_ms(expID, retention_time):
    """
    Search the MongoDB for a specific ms spectra with the corresponding Experiment ID and retention time
    :param expID: (MongoDB ObjectID) The experiment ID for the experiment of interest
    :param retention_time: (float) The specific retention time of interest
    :return: ms a dictionary containing the m/z and intensity as list of floats
    """
    client = MongoClient()
    db = client['nodbase']

    cursor = db['ms'].find({"expID": expID, "retentionTime": str(retention_time)})

    ms = {}

    for document in cursor:
        # Need to transform from list of strings to list of float in order to plot
        mz = [float(i) for i in document['m/z']]
        intensity = [float(i) for i in document['intensity']]
        print(intensity)
        
        ms.update({'m/z': mz,
                   'intensity': intensity})

    return ms


def search_chrom(expID):
    """
    This pulls the chromatogram from a known experiment ID
    :param expID: 
    :return: 
    """
    #  'ms_level': document['ms_level']}) Need to add this post testing
    chrom = {}
    client = MongoClient()
    db = client['nodbase']
    cursor = db['chrom'].find({'expID': expID, "ms_level": 1})

    for document in cursor:
        # Need to transform from list of strings to list of float in order to plot
        retentiontime = [float(i) for i in document['retentionTime']]
        bpi = document['bpi']
        totion = document['totion']

        chrom.update(
            {'expID': expID,
             'retentionTime': retentiontime,
             'bpi': bpi,
             'totion': totion})

    return chrom


def search_chrom_peak(entries):
    """
    Locates an experiment metadata based on the presence of a intensity threshold at a particular retention time
    At the moment it assumes that you are looking at the MS chromatogram, not the MS/MS one
    At the moment it searches based on bpi intensity
    :param entries a list containing the retention time and intensity cutoff
    :return: metadata (dict) from the found experiments
    """

    for entry in entries:
        retention_time = entry[0].get()
        intensity = float(entry[1].get())

    metadata = []
    expID = []
    client = MongoClient()
    db = client['nodbase']
    #TODO Add the intensity component
    cursor = db['chrom'].find({'retentionTime': {'$regex': '.*'+retention_time+'.*'},
                               'ms_level': 1})

    for document in cursor:
        # Check the value of the document at the matched position for the relative intensity level
        rt = document['retentionTime']
        bpi = document['bpi']
        index = [i for i, item in enumerate(rt) if item.startswith(retention_time)]

        for i in index:
            # Forcing as float is an artifact of some of the spectra bpi stored as strings.
            if float(bpi[i]) > intensity:
                expID.append(document['expID'])

    for id in set(expID):
        # Tracks the found experiment ID to the corresponding metadata.
        # The set function ensures that each experiment ID is searched only once
        cursor = db['meta'].find({'_id': id})

        for document in cursor:
            metadata.append(document)

    return metadata


def search_ms_peak(entries):
    """
    Locates an experiment metadata based on the presence of a intensity threshold at a particular m/z ratio
    :param entries
    :return: 
    """

    for entry in entries:
        mz = str(entry[0].get())
        intensity = (entry[1].get())

    print(mz)
    print(intensity)

    metadata = []
    expID = []
    rt = []
    client = MongoClient()
    db = client['nodbase']
    cursor = db['ms'].find({'m/z': {'$regex': '.*' + mz + '.*'}, 'intensity': {'$gt': intensity}})

    for document in cursor:
        # Pull the experiment ID for the found experiments
        expID.append(document['expID'])
        rt.append(document['retentionTime'])

    print(expID)
    print(rt)

    for id in set(expID):
        # Tracks the found experiment ID to the corresponding metadata.
        # The set function ensures that each experiment ID is searched only once
        cursor = db['meta'].find({'_id': id})

        for document in cursor:
            metadata.append(document)

    return metadata



