Feature: css3-fonts
 Scenario: font variant 003
   When launch "css3-fonts-app"
     And I go to "csswg/font-variant-003.htm"
     And I save the page to "font-variant-003"
    Then pic "font-variant-003" of baseline and result should be "100" similar if have results
