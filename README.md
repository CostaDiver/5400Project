<h2>Python scripts pull data from IMDB, reformat it into CSVs, upload it to an Azure database, then create an accesible Flask API to allow the database to be accessed and edited over the internet. Data is returned
and entered in the JSON format. Movie lookups and row deletions are done using the tconst key value.</h2>
<hr>
<h4>Available routes can be found below: </h4>
<ul>
  <li>/item&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-
  Returns the top 1000 movies sorted by release year and rating. Can be used as a get or post 
  (using JSON) function.
  </li>
  <li>/item/id&nbsp;&nbsp;&nbsp;-
  Returns a specific title where id is the tconst of the film. Can be used as a get or delete function.
  </li>
</ul>
