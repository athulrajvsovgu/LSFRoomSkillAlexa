# Steps to set up and test the skill

Follow the steps below to set up the skill in your [**Alexa Developer Console**](https://developer.amazon.com/de-DE/alexa/alexa-skills-kit):-
- Traverse to ***https://developer.amazon.com/alexa/console***

- Login using your ***Amazon account credentials***

- Select '***Create Skills***' option and follow the steps below to setup the skill (*[**refer**](../img/skillset.jpg) screenshot*):-
    - Enter the name as '***LSF Room Service***'
    - Set the language as '***English (US)***' *(which would be selected by default)*
    - Select the model as '***Custom***' *(which would be selected by default)*
    - Select the host method as '***Alexa - hosted (Python)***'
    - Select '***Create skill***'
    - Select the template as '***Start from Scratch***' *(which would be selected by default)*
    - Select '***Continue with template***'

- This opens up the Alexa Developer Console with the developer options for the '***LSF Room Service***' skill

- It has the following important [**tabs**](https://developer.amazon.com/en-US/docs/alexa/devconsole/about-the-developer-console.html):-
    - [**Build**](https://developer.amazon.com/en-US/docs/alexa/devconsole/build-your-skill.html)
    - [**Code**](https://developer.amazon.com/en-US/docs/alexa/custom-skills/use-the-alexa-skills-kit-samples.html)
    - [**Test**](https://developer.amazon.com/en-US/docs/alexa/devconsole/test-your-skill.html)
    - [**Distribution**](https://developer.amazon.com/en-US/docs/alexa/devconsole/launch-your-skill.html)
    - [**Certification**](https://developer.amazon.com/en-US/docs/alexa/devconsole/test-and-submit-your-skill.html)
    - [**Analytics**](https://developer.amazon.com/en-US/docs/alexa/devconsole/measure-skill-usage.html)

- Click on the '***Code***' tab and follow the following steps to setup the backend code (*[**refer**](../img/code.jpg) screenshot*):-
    - Use the codes from the files in *[**lambda**](../lambda/) folder*
    - Using the options '***New File***' and '***New Folder***' create the file / folder structure by giving the same name as in the lambda folder
    - To make use of the code it has to be deployed by selecting '***Deploy***' option

- To setup the interaction model click on the '***Build***' tab (*[**refer**](../img/build.jpg) screenshot*):-
    - Copy the code from the *[**interactionModels/custom**](../interactionModels/custom/) folder*
    - Click on the '***JSON Editor***' option and select '***Drag and drop a .json file***'
    - Paste the code into the editor field
    - Select the '***Build Model***' option to train and build the interaction model

- To test the skill click on the '***Test***' tab and follow the following steps (*[**refer**](../img/test.jpg) screenshot*):-
    - Set the '***Skill testing is enabled in***' as '***Development***'
    - In the '***Alexa Simulator***' set up a interaction with sample use case from the documention files to get response
    - The request and response could be seen in the '***JSON Input 1***' and '***JSON Output 1***' section

- To deploy and preview the skill '***Distribution***' and '***Certification***' steps has to be followed

- Lastly to analyse the performance and to preview the metrics check '***Analytics***'