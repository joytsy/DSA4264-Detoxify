# Application

The following sections showcase the different pages and features of LionGuard Pro Max.

## 1. Home Page

The homepage of our application serves as a central hub for users to access important information and navigate to other pages seamlessly. On the homepage, users will be able to find out what our application does and its goals, followed by a quick overview of the application's key features.

Additionally, the homepage features a navigation bar on the left of the page, containing buttons for Home, Classify Text and Analysis. Clicking on any of these buttons will redirect users to the corresponding pages, allowing for easy navigation throughout the application.

![home page](app_home_page.png)

## 2. Classify Text Page

The Classify Text Page enables users to classify text via various methods, either by manual classification for singular testing of comments or by uploading a CSV dataset for multiple testing of comments at one time. Users can also view the history of their past classifications, and discover more about the model used in this application.

### 2.1 Classifying Text by Manual Classification

On the Classify Text page, there is a Manual Classification tab that enables users to manually classify a comment by typing it into the chatbox, before clicking the Classify button below the box.

![manual classification tab](ct_manualclassification.png)

After clicking the Classify button, the predicted label will appear, thus showing the Language Intensity Classification of the comment. An example is shown below:

![hate 3](ct_mc_hate3.png)

<div align="center" style="font-size: 0.85em;">

Figure ####. Example of Classification Output when a Reddit Comment is Inputted

</div>

### 2.2 Classifying Text by Uploading CSV

Besides only being able to manually key in one comment at one time, users can upload a CSV file which enables them to test multiple comments at a go by clicking into the Upload CSV tab. The file can then be uploaded from the local device by clicking the Browse files button.

![upload csv tab](ct_uploadcsv.png)

### 2.3 History Tab

Clicking into the History tab enables users to view their past classifications, allowing them to track and review their work.

![history tab](ct_history.png)

### 2.4 Model Information Section

The Model Information section provides users with comprehensive details, including the model powering the application backend, how we fine-tuned it, and clear definitions and descriptions for each of our 7 classification categories. This gives users insight into how the model interprets and categorizes data. By understanding the model's foundations and classification criteria, users can make more informed interpretations of its outputs and have confidence in the underlying technology.

![model information](ct_modelinfo.png)

## 3. Analysis Page
