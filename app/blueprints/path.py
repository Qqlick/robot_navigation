
from flask import Blueprint, request, jsonify

path = Blueprint('path', __name__, url_prefix='/path')


@path.route('/', methods=["POST"])
def save_path_to_db():
    # """Add mood info to db
    #                ---
    #                tags:
    #                -
    #                produces:
    #                - application/json
    #                parameters:
    #                  - name: mood
    #                    description: Mood characteristics
    #                    in: body
    #                    required: true
    #                    schema:
    #                      $ref: "#/definitions/Mood"
    #                    example:
    #                         {
    #                         "location": {"lon": 34.23232323, "lat":45.222443},
    #                         "mood": 0,
    #                          "user": "1"
    #                         }
    #
    #                responses:
    #                 200:
    #                     description: Success.
    #                 500:
    #                     description: Mood and Location are required.
    #                definitions:
    #                   Mood:
    #                     type: object
    #                     required:
    #                       - mood
    #                       - location
    #                       - user
    #                     properties:
    #                       mood:
    #                         type: number
    #                         required: true
    #                         enum: [0, 1, 2]
    #                       location:
    #                         type: object
    #                         required: true
    #                         schema:
    #                           $ref: "#/definitions/Location"
    #                       user:
    #                         type: string
    #                         required: true
    #
    #                   Location:
    #                     type: object
    #                     required:
    #                       - lat
    #                       - lon
    #                     properties:
    #                       lat:
    #                         type: number
    #                         format: float
    #                         required: true
    #                       lon:
    #                         type: number
    #                         format: float
    #                         required: true
    #
    #                """

    # user = get_jwt_identity()

    location = request.json.pop('location')
    mood = int(request.json.get('mood'))

    return jsonify('Success', 200)

#
# @path.route('/mood_distribution')
# # @jwt_required  TODO enable in dev and production
# def get_mood_distribution():
#     """Returns mood distribution for a given user.
#                    ---
#                    tags:
#                    - API
#                    produces:
#                    - application/json
#
#                    responses:
#                     200:
#                         description: Success.
#                     500:
#                         description: Server failure
#                    """
#     # user = get_jwt_identity()
#     # TODO get actual user from JWT
#
#     res = es_aws.search(index='mood_data',
#                         body={"query": {'bool': {
#                             'must': [{
#
#                                 "match_phrase": {'user': "1"}}],
#                         }
#                         },
#                             'size': 0,
#                             "aggs": {
#                                 "mood_distribution": {
#                                     "terms": {
#                                         "field": "mood"
#
#                                     }
#                                 }
#                             },
#                         }
#
#                         )
#
#     moods = {0: "sad",
#              1: "neutral",
#              2: "happy"}
#     print(res)
#     buckets = res['aggregations']['mood_distribution']['buckets']
#     result = {moods[i['key']]: i['doc_count'] for i in buckets}
#     return jsonify({"mood_distribution": result, 'total': res['hits']['total']}), 200
#
#
# @api.route('/happy_places', methods=["POST"])
# # @jwt_required  TODO enable in dev and production
# def proximity_to_happy_places():
#     """Returns proximity to happy places from given location.
#                    ---
#                    tags:
#                    - API
#                    description: Returns three closest places where user was happy
#                    produces:
#                    - application/json
#                    parameters:
#                      - name: location
#                        description: Location(current location)
#                        in: body
#                        required: true
#                        schema:
#                          $ref: "#/definitions/Location"
#                    definitions:
#                       Location:
#                         type: object
#                         required:
#                           - lat
#                           - lon
#                         properties:
#                           lat:
#                             type: number
#                             format: float
#                             required: true
#                           lon:
#                             type: number
#                             format: float
#                             required: true
#
#
#                    responses:
#                     200:
#                         description: Success.
#                     500:
#                         description: Server failure
#                    """
#     try:
#         validate(request.json, schema=GeoPoint.get_point_schema())
#     except ValidationError as e:
#         return jsonify({'Validation error': e.message}), 500
#
#     res = es_aws.search(index='mood_data',
#                         body={
#                             "sort": [
#                                 {
#                                     "_geo_distance": {
#                                         "location": [request.json.get('lat'), request.json.get('lon')],
#                                         "order": "asc",
#                                         "unit": "m",
#                                         "mode": "min",
#                                         "distance_type": "arc",
#                                     }
#                                 }
#                             ],
#                             "query": {
#                                 "term": {"mood": 2}
#                             },
#                             "size": 3,
#
#                         })
#
#     results = res['hits']['hits']
#     for_return = {'closest_happy_places': list()}
#     for i in results:
#         source = i.get('_source')
#
#         location = source.pop('location')
#         time = source.pop('time')
#         distance = i.pop('sort')
#         # TODO retrieve address from location via https://geopy.readthedocs.io/en/latest/#data
#         # or Google API places
#         #
#         for_return['closest_happy_places'].append({'location': location,
#                                                    "time": time,
#                                                    "distance": distance})
#     return jsonify(for_return), 200
