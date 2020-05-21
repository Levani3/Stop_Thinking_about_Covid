<ion-header [translucent]="true">
  <ion-toolbar>
    <ion-title id="title">
      <img src="assets/img/title.PNG">
    </ion-title>
  </ion-toolbar>
</ion-header>

<ion-content [fullscreen]="true">
  <ion-header collapse="condense">
    <ion-toolbar>
      <ion-title size="large">Blank</ion-title>
    </ion-toolbar>
  </ion-header>
  <div id="image">
    <img src="assets/img/Censure.jpeg">
  </div>
  <div id="container">
    <form action="/action_page.php">
      <label for="myfile">Select a file: </label>
      <input type="file" id="myfile" name="myfile"><br><br>
      <ion-button color="danger" id="convert" expand="block">COVID-19 Censor!</ion-button>
    </form>
  </div>
    <div id="about">
        <h1>Instruccions for use</h1>
        <p>By using our censor you can easily censor COVID-19 related words in any mp4 videos and then download them for free - this service works for computers, tablets and mobile devices.</p>
        <p class="instruction"> 1. Select a video (.mp4)</p>
        <p class="instruction"> 2. Press <em>COVID-19 CENSOR!</em> button</p>
        <p>Now you can watch your censored video. ENJOY!</p>
    </div>
    <div id="footer">
        <hr />
    </div>

</ion-content>
