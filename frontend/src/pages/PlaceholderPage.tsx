type PlaceholderPageProps = {
  title: string;
  description: string;
};

export function PlaceholderPage({ title, description }: PlaceholderPageProps) {
  return (
    <section>
      <h1>{title}</h1>
      <p>{description}</p>
      <div className="notice" role="status">
        Ten widok jest gotowy do podłączenia API. Operacje na ClusterXL nie są zaimplementowane.
      </div>
    </section>
  );
}
