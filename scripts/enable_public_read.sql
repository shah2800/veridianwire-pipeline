-- Allow the website (anon key) to read published articles
ALTER TABLE published_articles ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Public read published articles" ON published_articles;
CREATE POLICY "Public read published articles"
  ON published_articles
  FOR SELECT
  TO anon, authenticated
  USING (true);
