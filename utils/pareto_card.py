from utils.queries import queries

def _generate_genre_html(genres):
  genre_html = "<h5>"
  number_genres = len(genres)
  if number_genres <= 2:
      genre_html += " --- ".join(genres)
  elif(number_genres <=6):
      for i in range(0, number_genres, 2):
          genre_html += " --- ".join(genres[i:i+2])
          genre_html += "<br>"
  else:
      for i in range(0, 6, 2):
        genre_html += " --- ".join(genres[i:i+2])
        genre_html += "<br>"
  genre_html += "</h5>"
  return genre_html

def generate(artist, genres, image):
    genre_html = _generate_genre_html(genres)

    topsongs = queries._get_top_songs(artist, 5)
    popularity_distribution = queries._get_distribution(artist, 'popularity')
    dance_distribution = queries._get_distribution(artist, 'danceability')
    emotion_distribution = queries._get_distribution(artist,'valence')
    energy_distribution = queries._get_distribution(artist, 'energy')    
    style_html = """
        <style>
          body { font-family: Helvetica, sans-serif; color: white; }
          .container { display: flex; flex-wrap: wrap; max-width: 700px; margin: auto;}
          .card { width: 300px; height: 500px; border: 2px solid #AAA; 
            background-image: linear-gradient(to bottom right, #133832, #552506);
            background-radius: 15px;
            border-image: linear-gradient(to right, #F1E1A4, #FFFFFF);
            border-image-slice: 1;
            flex:None; margin: 10px;
            }
          .card-header { text-align: center; justify-content: center; }
          .card-content { text-align: center; justify-content: center; margin-bottom: 10px; }
          .artist_pic { width:275px; height:275px; border-radius:50%; justify-content: center;}
          .front_info { font-family: Helvetica, sans-serif; word-wrap: break-word; max-width: 350px; margin: 0 auto;}
          h4{margin-top: 0; margin-bottom: 0; bottom: 0}
          p{margin-top: 0; margin-bottom: 0; }
          .top-songs { display: flex; flex-direction: column;}
          .song { display: flex; justify-content: space-between; padding-left: 10px;}
          .title {text-align: left; }
          .popularity { text-align: right; padding-right: 10px; }
          .metrics { text-align: bottom; }
          .metric { margin-bottom: 5px; }

          /* Responsive design */
          @media (max-width: 610px) {
            .container {
              flex-direction: column;
              align-items: center; 
            }
          }
        </style>
      """

    content_html = f"""
        <body>
        <div class="container"> 
        <div class="card">
          <div class="card-header">
            <h3>{artist}</h3>
          </div>
          <div class="card-content">
            <img src="{image}" class = "artist_pic">
            <div class="front_info">
              {genre_html}
              <h6>◍ - ◍ - ◍ - ◍ - ◍ - ◍ - ◍ - ◍ - ◍ - ◍ - ◍ - ◍</h6>
              <h4>Pareto Score:   30%</h4>
            </div>
          </div>
        </div>

        <div class="card">
            <div class="card-header">
                <h3>Most Popular</h3>
            </div>
            <div class="card-content">
              <div class="top-songs">
                <div class="song">
                  <span class="title">{topsongs[0][0]}</span>
                  <span class="popularity">{topsongs[0][1]}</span>
                </div>
                <div class="song">
                  <span class="title">{topsongs[1][0]}</span>
                  <span class="popularity">{topsongs[1][1]}</span>
                </div>
                <div class="song">
                  <span class="title">{topsongs[2][0]}</span>
                  <span class="popularity">{topsongs[2][1]}</span>
                </div>
                <div class="song">
                  <span class="title">{topsongs[3][0]}</span>
                  <span class="popularity">{topsongs[3][1]}</span>
                </div>
                <div class="song">
                  <span class="title">{topsongs[4][0]}</span>
                  <span class="popularity">{topsongs[4][1]}</span>
                </div>
              </div>
              <h6>◍ - ◍ - ◍ - ◍ - ◍ - ◍ - ◍ - ◍ - ◍ - ◍ - ◍ - ◍</h6 >
              <div class="card-header">
                <h3>Min | Mean | Max</h3>
              </div>
              <div class="metrics">
                <div class="metric"><strong>Popularity: </strong>{" - ".join(str(round(x)) for x in popularity_distribution)}</div>
                <div class="metric"><strong>Energy: </strong>{" - ".join(str(round(x,2)) for x in energy_distribution)}</div>
                <div class="metric"><strong>Danceability: </strong>{" - ".join(str(round(x,2)) for x in dance_distribution)}</div>
                <div class="metric"><strong>Emotion: </strong>{" - ".join(str(round(x,2)) for x in emotion_distribution)}</div>
              </div>
            </div>
        </div>
        </div>

        </body>
        """
    return (style_html, content_html)
      