Feature: css3-fonts
 Scenario: c523 font style 000
   When launch "css3-fonts-app"
     And I go to "csswg/c523-font-style-000.htm"
     And I save the page to "c523-font-style-000"
    Then pic "c523-font-style-000" of baseline and result should be "100" similar if have results
