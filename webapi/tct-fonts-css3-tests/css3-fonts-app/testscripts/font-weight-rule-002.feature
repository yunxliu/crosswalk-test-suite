Feature: css3-fonts
 Scenario: font weight rule 002
   When launch "css3-fonts-app"
     And I go to "csswg/font-weight-rule-002.htm"
     And I save the page to "font-weight-rule-002"
    Then pic "font-weight-rule-002" of baseline and result should be "100" similar if have results
