Feature: css3-fonts
 Scenario: font 009
   When launch "css3-fonts-app"
     And I go to "csswg/font-009.htm"
     And I save the page to "font-009"
    Then pic "font-009" of baseline and result should be "100" similar if have results
