Feature: css3-fonts
 Scenario: font style 004
   When launch "css3-fonts-app"
     And I go to "csswg/font-style-004.htm"
     And I save the page to "font-style-004"
    Then pic "font-style-004" of baseline and result should be "100" similar if have results
