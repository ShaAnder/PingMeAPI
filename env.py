import os

#hosting
os.environ["ALLOWED_HOSTS"] = "https://moments-api-shaander-19059c743c88.herokuapp.com"
os.environ["CLIENT_ORIGIN"] = "https://shaander-moments-67ea6a2bd534.herokuapp.com"
os.environ["CLIENT_ORIGIN_DEV"] = "https://pleasantly-quick-seasnail.ngrok-free.app"

#django dev
os.environ["SECRET_KEY"] = "django-insecure-%zugflh2lf0o2q0o&l_q!uujycqmkd1"
os.environ["DEV"] = "1"

#db
os.environ["DATABASE_URL"] = "postgresql://neondb_owner:y7LRT2ENqCfn@ep-bold-bush-a2n9ji22.eu-central-1.aws.neon.tech/fax_mural_slick_234263"


#email settings
os.environ["HOST_EMAIL"] = "pingmepp5@gmail.com"
os.environ["HOST_PW"] =  "lbnufsbomuyxzcqx"

# cloudinary api 
os.environ["CLOUDINARY_CLOUD_NAME"] = "dbldbdmuu"
os.environ["CLOUDINARY_API_KEY"] = "281637296264875"
os.environ["CLOUDINARY_API_SECRET"] = "o8KImcaPgCKsxHoRzJ7AxrotP4E"


# os.environ["CLOUDINARY_URL"] = "cloudinary://281637296264875:o8KImcaPgCKsxHoRzJ7AxrotP4E@dbldbdmuu"



