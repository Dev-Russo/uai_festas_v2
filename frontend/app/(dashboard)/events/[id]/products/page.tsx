"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { api } from "@/lib/api";
import { Commissioner, Product, ProductGroup } from "@/types";
import { ProductForm } from "@/components/products/ProductForm";
import { Table } from "@/components/ui/Table";
import { Modal } from "@/components/ui/Modal";
import { Button } from "@/components/ui/Button";
import { useAuth } from "@/lib/hooks/useAuth";

type GroupCardProps = {
  eventId: string;
  group: ProductGroup;
  products: Product[];
  selectedProductId: string;
  onChangeSelectedProduct: (groupId: string, productId: string) => void;
  onAddProduct: (groupId: string) => Promise<void>;
  onToggleGroup: (groupId: string, nextState: boolean) => Promise<void>;
  onToggleMembership: (groupId: string, productId: string, nextState: boolean) => Promise<void>;
  onRemoveMembership: (groupId: string, productId: string) => Promise<void>;
  onConfigureCommissioners: (groupId: string) => void;
  onDeleteGroup: (groupId: string) => Promise<void>;
  level?: number;
};

function GroupCard({
  eventId,
  group,
  products,
  selectedProductId,
  onChangeSelectedProduct,
  onAddProduct,
  onToggleGroup,
  onToggleMembership,
  onRemoveMembership,
  onConfigureCommissioners,
  onDeleteGroup,
  level = 0,
}: GroupCardProps) {
  const usedProductIds = new Set(group.memberships.map((membership) => membership.productId));
  const availableProducts = products.filter((product) => !usedProductIds.has(String(product.id)));

  return (
    <div
      className="card"
      style={{
        padding: "0.9rem",
        display: "grid",
        gap: "0.7rem",
        marginLeft: level > 0 ? `${level * 1.2}rem` : 0,
        borderLeft: level > 0 ? "3px solid var(--border)" : undefined,
      }}
    >
      <div style={{ display: "flex", justifyContent: "space-between", gap: "0.75rem", alignItems: "center", flexWrap: "wrap" }}>
        <div>
          <strong>{group.name}</strong>
          <p className="muted" style={{ margin: "0.2rem 0 0", fontSize: "0.86rem" }}>
            Grupo #{group.id} {group.isDefault ? "· Padrao" : ""} {group.isActive ? "· Ativo" : "· Inativo"}
          </p>
        </div>
        <div style={{ display: "flex", gap: "0.5rem", flexWrap: "wrap" }}>
          <button
            className="button-ghost"
            type="button"
            onClick={() => onConfigureCommissioners(group.id)}
            style={{ whiteSpace: "nowrap" }}
          >
            Comissarios
          </button>
          <button
            className="button-ghost"
            type="button"
            onClick={() => onToggleGroup(group.id, !group.isActive)}
            style={{ whiteSpace: "nowrap" }}
          >
            {group.isActive ? "Desativar grupo" : "Ativar grupo"}
          </button>
          <button
            className="button-ghost"
            type="button"
            onClick={() => onDeleteGroup(group.id)}
            style={{ whiteSpace: "nowrap", color: "#dc2626" }}
          >
            Excluir
          </button>
        </div>
      </div>

      <div style={{ display: "flex", gap: "0.5rem", flexWrap: "wrap" }}>
        <select
          className="input-field"
          value={selectedProductId}
          onChange={(event) => onChangeSelectedProduct(group.id, event.target.value)}
          style={{ minWidth: 240, maxWidth: 360 }}
        >
          <option value="">Adicionar produto ao grupo...</option>
          {availableProducts.map((product) => (
            <option key={product.id} value={String(product.id)}>
              {product.name} · {new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" }).format(product.price)}
            </option>
          ))}
        </select>
        <Button onClick={() => onAddProduct(group.id)} disabled={!selectedProductId}>Adicionar</Button>
      </div>

      <div style={{ overflowX: "auto" }}>
        <Table>
          <thead>
            <tr>
              <th>Produto</th>
              <th>Preco</th>
              <th>Status no Grupo</th>
              <th>Acoes</th>
            </tr>
          </thead>
          <tbody>
            {group.memberships.length === 0 ? (
              <tr>
                <td colSpan={4} className="muted">Nenhum produto neste grupo.</td>
              </tr>
            ) : (
              group.memberships.map((membership) => (
                <tr key={`${group.id}-${membership.productId}`}>
                  <td>{membership.product.name}</td>
                  <td>{new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" }).format(membership.product.price)}</td>
                  <td>
                    <label className="remember-row" style={{ userSelect: "none" }}>
                      <input
                        type="checkbox"
                        checked={membership.isActive}
                        onChange={(event) => onToggleMembership(group.id, membership.productId, event.target.checked)}
                      />
                      {membership.isActive ? "Ativo" : "Inativo"}
                    </label>
                  </td>
                  <td>
                    <button
                      className="button-ghost"
                      type="button"
                      onClick={() => onRemoveMembership(group.id, membership.productId)}
                    >
                      Remover
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </Table>
      </div>

      {group.children.length > 0 ? (
        <div style={{ display: "grid", gap: "0.7rem" }}>
          {group.children.map((child) => (
            <GroupCard
              key={child.id}
              eventId={eventId}
              group={child}
              products={products}
              selectedProductId={selectedProductId}
              onChangeSelectedProduct={onChangeSelectedProduct}
              onAddProduct={onAddProduct}
              onToggleGroup={onToggleGroup}
              onToggleMembership={onToggleMembership}
              onRemoveMembership={onRemoveMembership}
              onConfigureCommissioners={onConfigureCommissioners}
              onDeleteGroup={onDeleteGroup}
              level={level + 1}
            />
          ))}
        </div>
      ) : null}
    </div>
  );
}

export default function ProductsPage() {
  const { id } = useParams<{ id: string }>();
  const [products, setProducts] = useState<Product[]>([]);
  const [groups, setGroups] = useState<ProductGroup[]>([]);
  const [openProductModal, setOpenProductModal] = useState(false);
  const [openGroupModal, setOpenGroupModal] = useState(false);
  const [editingProduct, setEditingProduct] = useState<Product | null>(null);
  const { userType } = useAuth();
  const isCommissioner = userType === "commissioner";
  const [groupName, setGroupName] = useState("");
  const [groupParentId, setGroupParentId] = useState("");
  const [groupIsDefault, setGroupIsDefault] = useState(false);
  const [selectedProductByGroup, setSelectedProductByGroup] = useState<Record<string, string>>({});
  const [feedback, setFeedback] = useState<string>("");
  const [commissionersGroupId, setCommissionersGroupId] = useState<string | null>(null);
  const [allEventCommissioners, setAllEventCommissioners] = useState<Commissioner[]>([]);
  const [selectedCommissionerToAdd, setSelectedCommissionerToAdd] = useState("");

  function flattenGroups(list: ProductGroup[]): ProductGroup[] {
    return list.flatMap((group) => [group, ...flattenGroups(group.children)]);
  }

  const allGroups = flattenGroups(groups);

  async function loadProducts() {
    const data = await api.getProducts(String(id));
    setProducts(data);
  }

  async function loadGroups() {
    const data = await api.getProductGroups(String(id));
    setGroups(data);
  }

  function setGroupSelectedProduct(groupId: string, productId: string) {
    setSelectedProductByGroup((prev) => ({ ...prev, [groupId]: productId }));
  }

  async function handleDeleteGroup(groupId: string) {
    if (!window.confirm("Excluir este grupo? Esta acao nao pode ser desfeita.")) return;
    try {
      await api.deleteProductGroup(String(id), groupId);
      await loadGroups();
      setFeedback("Grupo excluido com sucesso.");
    } catch {
      setFeedback("Nao foi possivel excluir o grupo. Remova os subgrupos antes de excluir.");
    }
  }

  async function handleConfigureCommissioners(groupId: string) {
    try {
      const data = await api.getCommissioners(String(id));
      setAllEventCommissioners(data);
    } catch {
      setAllEventCommissioners([]);
    }
    setSelectedCommissionerToAdd("");
    setCommissionersGroupId(groupId);
  }

  async function handleAddCommissionerToGroup() {
    if (!selectedCommissionerToAdd || !commissionersGroupId) return;
    const commissioner = allEventCommissioners.find((c) => c.id === selectedCommissionerToAdd);
    if (commissioner && commissioner.commissionerGroupId != null && String(commissioner.commissionerGroupId) !== commissionersGroupId) {
      const sourceGroupName = allGroups.find((g) => g.id === String(commissioner.commissionerGroupId))?.name ?? `Grupo #${commissioner.commissionerGroupId}`;
      const targetGroupName = allGroups.find((g) => g.id === commissionersGroupId)?.name ?? `Grupo #${commissionersGroupId}`;
      const confirmed = window.confirm(`${commissioner.name} ja esta em "${sourceGroupName}". Mover para "${targetGroupName}"?`);
      if (!confirmed) return;
    }
    try {
      await api.updateCommissioner(String(id), selectedCommissionerToAdd, {
        commissionerGroupId: Number(commissionersGroupId),
      });
      const data = await api.getCommissioners(String(id));
      setAllEventCommissioners(data);
      setSelectedCommissionerToAdd("");
    } catch {
      setFeedback("Nao foi possivel adicionar o comissario ao grupo.");
    }
  }

  async function handleRemoveCommissionerFromGroup(commissionerId: string) {
    try {
      await api.updateCommissioner(String(id), commissionerId, {
        commissionerGroupId: null,
      });
      const data = await api.getCommissioners(String(id));
      setAllEventCommissioners(data);
    } catch {
      setFeedback("Nao foi possivel remover o comissario do grupo.");
    }
  }

  async function handleCreateGroup() {
    if (!groupName.trim()) {
      setFeedback("Informe o nome do grupo.");
      return;
    }

    try {
      await api.createProductGroup(String(id), {
        name: groupName.trim(),
        parentGroupId: groupParentId || null,
        isDefault: groupIsDefault,
      });
      setGroupName("");
      setGroupParentId("");
      setGroupIsDefault(false);
      setOpenGroupModal(false);
      setFeedback("Grupo criado com sucesso.");
      await loadGroups();
    } catch {
      setFeedback("Nao foi possivel criar o grupo.");
    }
  }

  async function handleAddProductToGroup(groupId: string) {
    const productId = selectedProductByGroup[groupId];
    if (!productId) {
      return;
    }
    try {
      await api.addProductToGroup(String(id), groupId, productId);
      setGroupSelectedProduct(groupId, "");
      await loadGroups();
      setFeedback("Produto adicionado ao grupo.");
    } catch {
      setFeedback("Nao foi possivel adicionar o produto ao grupo.");
    }
  }

  async function handleToggleGroup(groupId: string, nextState: boolean) {
    try {
      await api.updateProductGroup(String(id), groupId, { isActive: nextState });
      await loadGroups();
      setFeedback(nextState ? "Grupo ativado." : "Grupo desativado.");
    } catch {
      setFeedback("Nao foi possivel atualizar o grupo.");
    }
  }

  async function handleToggleMembership(groupId: string, productId: string, nextState: boolean) {
    try {
      await api.toggleProductInGroup(String(id), groupId, productId, nextState);
      await loadGroups();
      setFeedback(nextState ? "Produto ativado no grupo." : "Produto desativado no grupo.");
    } catch {
      setFeedback("Nao foi possivel alterar o status do produto no grupo.");
    }
  }

  async function handleRemoveMembership(groupId: string, productId: string) {
    try {
      await api.removeProductFromGroup(String(id), groupId, productId);
      await loadGroups();
      setFeedback("Produto removido do grupo.");
    } catch {
      setFeedback("Nao foi possivel remover o produto do grupo.");
    }
  }

  useEffect(() => {
    let isMounted = true;

    const requests = isCommissioner
      ? [api.getProducts(String(id)), Promise.resolve([])] as const
      : [api.getProducts(String(id)), api.getProductGroups(String(id))] as const;

    Promise.all(requests)
      .then(([productsData, groupsData]) => {
        if (!isMounted) return;
        setProducts(productsData as Product[]);
        setGroups(groupsData as ProductGroup[]);
      })
      .catch(() => {
        if (!isMounted) return;
        setProducts([]);
        setGroups([]);
      });

    return () => {
      isMounted = false;
    };
  }, [id, isCommissioner]);

  return (
    <main style={{ display: "grid", gap: "1rem" }}>
      <section className="card" style={{ padding: "1rem", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <div>
          <p className="muted" style={{ margin: 0 }}>Eventos &gt; {id} &gt; Lotes</p>
          <h1 style={{ margin: "0.35rem 0 0" }}>Lotes de Ingresso</h1>
        </div>
        {!isCommissioner && (
          <div style={{ display: "flex", gap: "0.5rem", flexWrap: "wrap" }}>
            <Button onClick={() => setOpenGroupModal(true)}>+ Novo Grupo</Button>
            <Button onClick={() => setOpenProductModal(true)}>+ Novo Lote</Button>
          </div>
        )}
      </section>

      {feedback ? (
        <section className="card" style={{ padding: "0.8rem 1rem" }}>
          <p className="muted" style={{ margin: 0 }}>{feedback}</p>
        </section>
      ) : null}

      <section className="card" style={{ padding: "1rem" }}>
        <h2 style={{ marginTop: 0 }}>Lotes</h2>
        <Table>
          <thead>
            <tr>
              <th>Nome</th><th>Preco</th><th>Disponivel</th><th>Periodo</th><th>Acoes</th>
            </tr>
          </thead>
          <tbody>
            {products.map((product) => (
              <tr key={product.id}>
                <td>{product.name}</td>
                <td>{new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" }).format(product.price)}</td>
                <td>{product.quantity ?? "-"}</td>
                <td>
                  {product.startDate || product.endDate
                    ? `${product.startDate ? new Date(product.startDate).toLocaleDateString("pt-BR") : "?"} → ${product.endDate ? new Date(product.endDate).toLocaleDateString("pt-BR") : "?"}`
                    : "-"}
                </td>
                <td>
                  {!isCommissioner && (
                    <button className="button-ghost" type="button" onClick={() => setEditingProduct(product)}>Editar</button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </Table>
      </section>

      {!isCommissioner && (
        <section className="card" style={{ padding: "1rem", display: "grid", gap: "0.9rem" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", gap: "0.7rem", flexWrap: "wrap" }}>
            <div>
              <h2 style={{ margin: 0 }}>Grupos de Acesso</h2>
              <p className="muted" style={{ margin: "0.35rem 0 0", fontSize: "0.9rem" }}>
                Defina quais lotes ficam disponiveis para cada grupo de comissarios.
              </p>
            </div>
            <Button onClick={() => setOpenGroupModal(true)}>Criar grupo</Button>
          </div>

          {groups.length === 0 ? (
            <p className="muted" style={{ margin: 0 }}>Nenhum grupo criado para este evento.</p>
          ) : (
            <div style={{ display: "grid", gap: "0.8rem" }}>
              {groups.map((group) => (
                <GroupCard
                  key={group.id}
                  eventId={String(id)}
                  group={group}
                  products={products}
                  selectedProductId={selectedProductByGroup[group.id] ?? ""}
                  onChangeSelectedProduct={setGroupSelectedProduct}
                  onAddProduct={handleAddProductToGroup}
                  onToggleGroup={handleToggleGroup}
                  onToggleMembership={handleToggleMembership}
                  onRemoveMembership={handleRemoveMembership}
                  onConfigureCommissioners={handleConfigureCommissioners}
                  onDeleteGroup={handleDeleteGroup}
                />
              ))}
            </div>
          )}
        </section>
      )}

      {!isCommissioner && (
        <Modal open={openProductModal} title="Novo lote" onClose={() => setOpenProductModal(false)}>
          <ProductForm
            onSubmit={async (payload) => {
              await api.createProduct(String(id), payload);
              setOpenProductModal(false);
              loadProducts();
            }}
          />
        </Modal>
      )}

      {editingProduct && (
        <Modal open={!!editingProduct} title="Editar lote" onClose={() => setEditingProduct(null)}>
          <ProductForm
            initialValues={{
              name: editingProduct.name,
              price: editingProduct.price,
              quantity: editingProduct.quantity,
              startDate: editingProduct.startDate,
              endDate: editingProduct.endDate,
            }}
            onSubmit={async (payload) => {
              await api.updateProduct(String(id), String(editingProduct.id), payload);
              setEditingProduct(null);
              loadProducts();
            }}
          />
        </Modal>
      )}

      {!isCommissioner && (
        <Modal open={openGroupModal} title="Novo grupo de acesso" onClose={() => setOpenGroupModal(false)}>
          <div style={{ display: "grid", gap: "0.7rem" }}>
            <div style={{ display: "grid", gap: "0.3rem" }}>
              <label htmlFor="group-name">Nome do grupo</label>
              <input
                id="group-name"
                className="input-field"
                value={groupName}
                onChange={(event) => setGroupName(event.target.value)}
                placeholder="Ex.: Comissarios externos"
              />
            </div>

            <div style={{ display: "grid", gap: "0.3rem" }}>
              <label htmlFor="group-parent">Grupo pai (opcional)</label>
              <select
                id="group-parent"
                className="input-field"
                value={groupParentId}
                onChange={(event) => setGroupParentId(event.target.value)}
              >
                <option value="">Sem grupo pai</option>
                {allGroups.map((group) => (
                  <option key={group.id} value={group.id}>
                    {group.name}
                  </option>
                ))}
              </select>
            </div>

            <label className="remember-row" style={{ userSelect: "none" }}>
              <input
                type="checkbox"
                checked={groupIsDefault}
                onChange={(event) => setGroupIsDefault(event.target.checked)}
              />
              Definir como grupo padrao
            </label>

            <div style={{ display: "flex", justifyContent: "flex-end", gap: "0.5rem" }}>
              <button className="button-ghost" type="button" onClick={() => setOpenGroupModal(false)}>Cancelar</button>
              <Button onClick={handleCreateGroup}>Criar grupo</Button>
            </div>
          </div>
        </Modal>
      )}
      {commissionersGroupId !== null && (() => {
        const groupName = allGroups.find((g) => g.id === commissionersGroupId)?.name ?? `Grupo #${commissionersGroupId}`;
        const inGroup = allEventCommissioners.filter((c) => c.commissionerGroupId === commissionersGroupId);
        const notInGroup = allEventCommissioners.filter((c) => c.commissionerGroupId !== commissionersGroupId);
        return (
          <Modal
            open={commissionersGroupId !== null}
            title={`Comissarios — ${groupName}`}
            onClose={() => setCommissionersGroupId(null)}
          >
            <div style={{ display: "grid", gap: "1rem" }}>
              <div style={{ display: "flex", gap: "0.5rem" }}>
                <select
                  className="input-field"
                  value={selectedCommissionerToAdd}
                  onChange={(e) => setSelectedCommissionerToAdd(e.target.value)}
                  style={{ flex: 1 }}
                >
                  <option value="">Selecionar comissario...</option>
                  {notInGroup.map((c) => (
                    <option key={c.id} value={c.id}>
                      {c.name} ({c.username})
                    </option>
                  ))}
                </select>
                <Button onClick={handleAddCommissionerToGroup} disabled={!selectedCommissionerToAdd}>
                  Adicionar
                </Button>
              </div>

              {inGroup.length === 0 ? (
                <p className="muted" style={{ margin: 0 }}>Nenhum comissario neste grupo.</p>
              ) : (
                <Table>
                  <thead>
                    <tr>
                      <th>Nome</th>
                      <th>Usuario</th>
                      <th>Acoes</th>
                    </tr>
                  </thead>
                  <tbody>
                    {inGroup.map((c) => (
                      <tr key={c.id}>
                        <td>{c.name}</td>
                        <td>{c.username}</td>
                        <td>
                          <button
                            className="button-ghost"
                            type="button"
                            onClick={() => handleRemoveCommissionerFromGroup(c.id)}
                          >
                            Remover
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </Table>
              )}
            </div>
          </Modal>
        );
      })()}
    </main>
  );
}
