Feature: css3-fonts
 Scenario: font 006
   When launch "css3-fonts-app"
     And I go to "csswg/font-006.htm"
     And I save the page to "font-006"
    Then pic "font-006" of baseline and result should be "100" similar if have results
