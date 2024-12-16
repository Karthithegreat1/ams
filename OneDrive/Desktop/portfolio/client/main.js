document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('downloadButton').addEventListener('click', function() {
      const resumeURL = 'M.KARTHIK.pdf';
      const resumeFileName = 'KARTHIK.M_Resume.pdf';
      const anchor = document.createElement('a');
      anchor.href = resumeURL;
      anchor.download = resumeFileName;
      document.body.appendChild(anchor);
      anchor.click();
      document.body.removeChild(anchor);
    });
  });
  